"""
Database Module for Business Card Extraction
Supports MySQL, PostgreSQL, and SQLite using SQLAlchemy.
"""

from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
import pandas as pd
import logging
from typing import Dict, List, Optional
import csv
import io
from datetime import datetime
import os


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager for business card extraction application."""
    
    def __init__(self, db_type='mysql', host='localhost', user='root', password='root', database='business_cards', port=None, sqlite_path=None):
        """
        Initialize database connection.
        
        Args:
            db_type (str): Database type ('mysql', 'postgresql', 'sqlite')
            host (str): MySQL host address
            user (str): MySQL username
            password (str): MySQL password
            database (str): Database name
            port (int): MySQL port
            sqlite_path (str): Path to SQLite database file
        """
        # Normalize database type to lowercase
        self.db_type = db_type.lower() if db_type else 'mysql'
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.sqlite_path = sqlite_path
        self.engine = None
        self.connect()
    
    def get_connection_string(self):
        if self.db_type == 'mysql':
            port = self.port or 3306
            return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{port}/{self.database}"
        elif self.db_type == 'postgresql':
            port = self.port or 5432
            return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{port}/{self.database}"
        elif self.db_type == 'sqlite':
            path = self.sqlite_path or f"{self.database}.db"
            return f"sqlite:///{path}"
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}. Supported types: mysql, postgresql, sqlite")
    
    def connect(self):
        """
        Establish database connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            conn_str = self.get_connection_string()
            self.engine = create_engine(conn_str, echo=False, future=True)
            logger.info(f"Connected to {self.db_type} database.")
            self.ensure_contacts_table()
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            self.engine = None
            return False
    
    def ensure_contacts_table(self):
        try:
            meta = MetaData()
            contacts = Table(
                'contacts', meta,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('name', String(100)),
                Column('designation', String(100)),
                Column('company', String(100)),
                Column('phone', String(50)),
                Column('email', String(100)),
                Column('website', String(100)),
                Column('address', String(255)),
                Column('created_at', TIMESTAMP)
            )
            meta.create_all(self.engine)
            logger.info("Ensured contacts table exists.")
        except Exception as e:
            logger.error(f"Error ensuring contacts table: {e}")
    
    def disconnect(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
    
    def test_connection(self):
        """
        Test database connection.
        
        Returns:
            bool: True if connection is working, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def check_duplicates(self, data: Dict) -> Dict:
        """
        Check for duplicate contacts based on name, phone, and email.
        
        Args:
            data (dict): Dictionary containing business card fields
            
        Returns:
            dict: Dictionary with duplicate information
                {
                    'has_duplicates': bool,
                    'duplicates': list of duplicate records,
                    'duplicate_fields': list of fields that match
                }
        """
        try:
            duplicates = []
            duplicate_fields = []
            
            # Get name, phone, and email from the new data
            new_name = data.get('name', '').strip().lower()
            new_phones = [phone.strip().lower() for phone in data.get('phone', []) if phone.strip()]
            new_emails = [email.strip().lower() for email in data.get('email', []) if email.strip()]
            
            # Get all existing contacts
            existing_contacts = self.get_all_contacts()
            if existing_contacts is None or len(existing_contacts) == 0:
                return {
                    'has_duplicates': False,
                    'duplicates': [],
                    'duplicate_fields': []
                }
            
            for _, contact in existing_contacts.iterrows():
                match_fields = []
                
                # Check name match
                existing_name = str(contact.get('name', '')).strip().lower()
                if new_name and existing_name and new_name == existing_name:
                    match_fields.append('name')
                
                # Check phone matches
                existing_phones = []
                if contact.get('phone'):
                    existing_phones = [phone.strip().lower() for phone in str(contact['phone']).split(',') if phone.strip()]
                
                for new_phone in new_phones:
                    for existing_phone in existing_phones:
                        if new_phone and existing_phone and new_phone == existing_phone:
                            if 'phone' not in match_fields:
                                match_fields.append('phone')
                
                # Check email matches
                existing_emails = []
                if contact.get('email'):
                    existing_emails = [email.strip().lower() for email in str(contact['email']).split(',') if email.strip()]
                
                for new_email in new_emails:
                    for existing_email in existing_emails:
                        if new_email and existing_email and new_email == existing_email:
                            if 'email' not in match_fields:
                                match_fields.append('email')
                
                # If any field matches, add to duplicates
                if match_fields:
                    duplicates.append({
                        'id': contact.get('id'),
                        'name': contact.get('name'),
                        'designation': contact.get('designation'),
                        'company': contact.get('company'),
                        'phone': contact.get('phone'),
                        'email': contact.get('email'),
                        'website': contact.get('website'),
                        'address': contact.get('address'),
                        'created_at': contact.get('created_at'),
                        'match_fields': match_fields
                    })
                    duplicate_fields.extend(match_fields)
            
            # Remove duplicate field entries
            duplicate_fields = list(set(duplicate_fields))
            
            return {
                'has_duplicates': len(duplicates) > 0,
                'duplicates': duplicates,
                'duplicate_fields': duplicate_fields
            }
            
        except Exception as e:
            logger.error(f"Error checking duplicates: {e}")
            return {
                'has_duplicates': False,
                'duplicates': [],
                'duplicate_fields': []
            }
    
    def store_in_db(self, data: Dict) -> bool:
        """
        Store business card data in the database.
        
        Args:
            data (dict): Dictionary containing business card fields
            
        Returns:
            bool: True if data stored successfully, False otherwise
        """
        try:
            df = pd.DataFrame([data])
            df['phone'] = [', '.join(data.get('phone', []))]
            df['email'] = [', '.join(data.get('email', []))]
            df['website'] = [', '.join(data.get('website', []))]
            df['created_at'] = pd.Timestamp.now()
            df.to_sql('contacts', self.engine, if_exists='append', index=False)
            return True
        except Exception as e:
            logger.error(f"Error storing data: {e}")
            return False
    
    def get_all_contacts(self) -> Optional[pd.DataFrame]:
        """
        Retrieve all contacts from the database.
        
        Returns:
            pandas.DataFrame: DataFrame containing all contacts, or None if error
        """
        try:
            return pd.read_sql('SELECT * FROM contacts ORDER BY created_at DESC', self.engine)
        except Exception as e:
            logger.error(f"Error fetching contacts: {e}")
            return None
    
    def export_to_csv(self, filepath: str = None) -> Optional[str]:
        """
        Export all contacts to CSV file.
        
        Args:
            filepath (str): Path to save CSV file. If None, generates timestamped filename.
            
        Returns:
            str: Path to the exported CSV file, or None if error
        """
        try:
            df = self.get_all_contacts()
            if df is None or len(df) == 0:
                logger.warning("No contacts to export")
                return None
            
            if filepath is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = f"contacts_export_{timestamp}.csv"
            
            # Export to CSV
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Successfully exported {len(df)} contacts to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting contacts to CSV: {e}")
            return None
    
    def export_to_excel(self, filepath: str = None) -> Optional[str]:
        """
        Export all contacts to Excel file.
        
        Args:
            filepath (str): Path to save Excel file. If None, generates timestamped filename.
            
        Returns:
            str: Path to the exported Excel file, or None if error
        """
        try:
            df = self.get_all_contacts()
            if df is None or len(df) == 0:
                logger.warning("No contacts to export")
                return None
            
            if filepath is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = f"contacts_export_{timestamp}.xlsx"
            
            # Export to Excel
            df.to_excel(filepath, index=False, engine='openpyxl')
            logger.info(f"Successfully exported {len(df)} contacts to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting contacts to Excel: {e}")
            return None
    
    def import_from_csv(self, filepath: str, skip_duplicates: bool = True) -> Dict:
        """
        Import contacts from CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            skip_duplicates (bool): Whether to skip duplicate entries
            
        Returns:
            dict: Import results with success count, error count, and details
        """
        try:
            if not self.test_connection():
                raise Exception("Database connection failed")
            
            # Read CSV file
            df = pd.read_csv(filepath, encoding='utf-8')
            
            if len(df) == 0:
                return {
                    'success_count': 0,
                    'error_count': 0,
                    'total_count': 0,
                    'errors': [],
                    'message': 'CSV file is empty'
                }
            
            # Validate required columns
            required_columns = ['name', 'designation', 'company', 'phone', 'email', 'website', 'address']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    'success_count': 0,
                    'error_count': 0,
                    'total_count': len(df),
                    'errors': [f"Missing required columns: {', '.join(missing_columns)}"],
                    'message': 'CSV file missing required columns'
                }
            
            cursor = self.engine.connect().execute(text("INSERT INTO contacts (name, designation, company, phone, email, website, address) VALUES (:name, :designation, :company, :phone, :email, :website, :address)"))
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Prepare data
                    name = str(row.get('name', '')).strip()
                    designation = str(row.get('designation', '')).strip()
                    company = str(row.get('company', '')).strip()
                    phone = str(row.get('phone', '')).strip()
                    email = str(row.get('email', '')).strip()
                    website = str(row.get('website', '')).strip()
                    address = str(row.get('address', '')).strip()
                    
                    # Skip empty rows
                    if not name and not company:
                        continue
                    
                    # Check for duplicates if skip_duplicates is True
                    if skip_duplicates:
                        duplicate_query = text("SELECT id FROM contacts WHERE (name = :name AND company = :company) OR (email = :email AND email != '')")
                        cursor.execute(duplicate_query, {'name': name, 'company': company, 'email': email})
                        if cursor.rowcount > 0:
                            continue
                    
                    # Insert contact
                    cursor.execute(text("INSERT INTO contacts (name, designation, company, phone, email, website, address) VALUES (:name, :designation, :company, :phone, :email, :website, :address)"), {'name': name, 'designation': designation, 'company': company, 'phone': phone, 'email': email, 'website': website, 'address': address})
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            cursor.close()
            
            result = {
                'success_count': success_count,
                'error_count': error_count,
                'total_count': len(df),
                'errors': errors,
                'message': f'Successfully imported {success_count} contacts'
            }
            
            logger.info(f"Import completed: {success_count} successful, {error_count} errors")
            return result
            
        except Exception as e:
            logger.error(f"Error importing contacts from CSV: {e}")
            return {
                'success_count': 0,
                'error_count': 0,
                'total_count': 0,
                'errors': [str(e)],
                'message': f'Import failed: {str(e)}'
            }
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Dict]:
        """
        Retrieve a specific contact by ID.
        
        Args:
            contact_id (int): Contact ID to retrieve
            
        Returns:
            dict: Contact data dictionary, or None if not found
        """
        try:
            if not self.test_connection():
                raise Exception("Database connection failed")
            
            cursor = self.engine.connect().execute(text("SELECT * FROM contacts WHERE id = :contact_id"))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                # Convert comma-separated strings back to lists
                result['phone'] = result['phone'].split(', ') if result['phone'] else []
                result['email'] = result['email'].split(', ') if result['email'] else []
                result['website'] = result['website'].split(', ') if result['website'] else []
                
                logger.info(f"Retrieved contact ID {contact_id}")
                return result
            else:
                logger.warning(f"Contact ID {contact_id} not found")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving contact from database: {e}")
            return None
    
    def delete_contact(self, contact_id: int) -> bool:
        """
        Delete a contact by ID.
        
        Args:
            contact_id (int): Contact ID to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            with self.engine.begin() as conn:
                result = conn.execute(text("DELETE FROM contacts WHERE id = :contact_id"), {'contact_id': contact_id})
                logger.info(f"Deleted contact id {contact_id}, rows affected: {result.rowcount}")
                return result.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting contact: {e}")
            return False
    
    def get_export_template(self) -> str:
        """
        Get CSV template for import.
        
        Returns:
            str: CSV template content
        """
        template_data = [
            ['name', 'designation', 'company', 'phone', 'email', 'website', 'address'],
            ['John Doe', 'Software Engineer', 'Tech Corp', '(555) 123-4567', 'john@techcorp.com', 'www.techcorp.com', '123 Main St, City, State 12345'],
            ['Jane Smith', 'Marketing Manager', 'Marketing Inc', '(555) 987-6543', 'jane@marketing.com', 'www.marketing.com', '456 Oak Ave, Town, State 67890']
        ]
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(template_data)
        
        return output.getvalue()

    def update_contact(self, contact_id: int, data: Dict) -> bool:
        """
        Update a contact by ID.
        
        Args:
            contact_id (int): Contact ID to update
            data (dict): Dictionary containing updated contact fields
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            if not self.test_connection():
                raise Exception("Database connection failed")
            
            # Prepare data for update
            update_data = {
                'name': data.get('name', ''),
                'designation': data.get('designation', ''),
                'company': data.get('company', ''),
                'phone': ', '.join(data.get('phone', [])) if isinstance(data.get('phone'), list) else data.get('phone', ''),
                'email': ', '.join(data.get('email', [])) if isinstance(data.get('email'), list) else data.get('email', ''),
                'website': ', '.join(data.get('website', [])) if isinstance(data.get('website'), list) else data.get('website', ''),
                'address': data.get('address', ''),
                'contact_id': contact_id
            }
            
            query = text("""
            UPDATE contacts 
            SET name = :name, designation = :designation, company = :company, 
                phone = :phone, email = :email, website = :website, address = :address
            WHERE id = :contact_id
            """)
            
            with self.engine.begin() as conn:
                result = conn.execute(query, update_data)
                logger.info(f"Updated contact ID {contact_id}, rows affected: {result.rowcount}")
                return result.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error updating contact: {e}")
            return False

    def merge_contacts(self, contact1_id: int, contact2_id: int) -> bool:
        """
        Merge two duplicate contacts by combining their information.
        
        Args:
            contact1_id (int): ID of the first contact (will be kept)
            contact2_id (int): ID of the second contact (will be deleted)
            
        Returns:
            bool: True if merge successful, False otherwise
        """
        try:
            # Get both contacts
            contact1 = self.get_contact_by_id(contact1_id)
            contact2 = self.get_contact_by_id(contact2_id)
            
            if not contact1 or not contact2:
                logger.error("One or both contacts not found")
                return False
            
            # Merge the data intelligently
            merged_data = {}
            
            # Name: prefer non-empty, longer name
            name1 = contact1.get('name', '').strip()
            name2 = contact2.get('name', '').strip()
            merged_data['name'] = name1 if len(name1) >= len(name2) else name2
            
            # Company: prefer non-empty, longer company name
            company1 = contact1.get('company', '').strip()
            company2 = contact2.get('company', '').strip()
            merged_data['company'] = company1 if len(company1) >= len(company2) else company2
            
            # Designation: prefer non-empty, longer designation
            designation1 = contact1.get('designation', '').strip()
            designation2 = contact2.get('designation', '').strip()
            merged_data['designation'] = designation1 if len(designation1) >= len(designation2) else designation2
            
            # Address: prefer non-empty, longer address
            address1 = contact1.get('address', '').strip()
            address2 = contact2.get('address', '').strip()
            merged_data['address'] = address1 if len(address1) >= len(address2) else address2
            
            # Phone: combine unique phone numbers
            phones1 = [phone.strip() for phone in contact1.get('phone', '').split(',') if phone.strip()]
            phones2 = [phone.strip() for phone in contact2.get('phone', '').split(',') if phone.strip()]
            all_phones = list(set(phones1 + phones2))  # Remove duplicates
            merged_data['phone'] = ', '.join(all_phones)
            
            # Email: combine unique email addresses
            emails1 = [email.strip() for email in contact1.get('email', '').split(',') if email.strip()]
            emails2 = [email.strip() for email in contact2.get('email', '').split(',') if email.strip()]
            all_emails = list(set(emails1 + emails2))  # Remove duplicates
            merged_data['email'] = ', '.join(all_emails)
            
            # Website: combine unique websites
            websites1 = [website.strip() for website in contact1.get('website', '').split(',') if website.strip()]
            websites2 = [website.strip() for website in contact2.get('website', '').split(',') if website.strip()]
            all_websites = list(set(websites1 + websites2))  # Remove duplicates
            merged_data['website'] = ', '.join(all_websites)
            
            # Update contact1 with merged data
            success = self.update_contact(contact1_id, merged_data)
            if not success:
                logger.error("Failed to update contact1 with merged data")
                return False
            
            # Delete contact2
            success = self.delete_contact(contact2_id)
            if not success:
                logger.error("Failed to delete contact2 after merge")
                return False
            
            logger.info(f"Successfully merged contacts {contact1_id} and {contact2_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error merging contacts: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()


def set_db_config(db_type, host, user, password, database, port=None, sqlite_path=None):
    """Set database configuration and reinitialize the global database manager."""
    global db_manager
    try:
        # Normalize database type to lowercase
        db_type_normalized = db_type.lower() if db_type else 'mysql'
        
        # Create new database manager instance
        db_manager = DatabaseManager(
            db_type=db_type_normalized,
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            sqlite_path=sqlite_path
        )
        
        logger.info(f"Database configuration updated: {db_type_normalized}")
        return True
    except Exception as e:
        logger.error(f"Error setting database configuration: {e}")
        # Fallback to default configuration
        db_manager = DatabaseManager()
        return False


def store_in_db(data: Dict) -> bool:
    """
    Store business card data in the database.
    
    Args:
        data (dict): Dictionary containing business card fields
        
    Returns:
        bool: True if data stored successfully, False otherwise
    """
    return db_manager.store_in_db(data)


def get_all_contacts() -> Optional[pd.DataFrame]:
    """
    Retrieve all contacts from the database.
    
    Returns:
        pandas.DataFrame: DataFrame containing all contacts, or None if error
    """
    return db_manager.get_all_contacts()


def export_to_csv(filepath: str = None) -> Optional[str]:
    """
    Export all contacts to CSV file.
    
    Args:
        filepath (str): Path to save CSV file. If None, generates timestamped filename.
        
    Returns:
        str: Path to the exported CSV file, or None if error
    """
    return db_manager.export_to_csv(filepath)


def export_to_excel(filepath: str = None) -> Optional[str]:
    """
    Export all contacts to Excel file.
    
    Args:
        filepath (str): Path to save Excel file. If None, generates timestamped filename.
        
    Returns:
        str: Path to the exported Excel file, or None if error
    """
    return db_manager.export_to_excel(filepath)


def import_from_csv(filepath: str, skip_duplicates: bool = True) -> Dict:
    """
    Import contacts from CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        skip_duplicates (bool): Whether to skip duplicate entries
        
    Returns:
        dict: Import results with success count, error count, and details
    """
    return db_manager.import_from_csv(filepath, skip_duplicates)


def get_export_template() -> str:
    """
    Get CSV template for import.
    
    Returns:
        str: CSV template content
    """
    return db_manager.get_export_template()


def update_contact(contact_id: int, data: Dict) -> bool:
    """
    Update a contact by ID.
    
    Args:
        contact_id (int): Contact ID to update
        data (dict): Dictionary containing updated contact fields
        
    Returns:
        bool: True if updated successfully, False otherwise
    """
    return db_manager.update_contact(contact_id, data)


if __name__ == "__main__":
    # Test database connection
    try:
        if db_manager.test_connection():
            print("Database connection test successful")
            
            # Test retrieving contacts
            contacts = get_all_contacts()
            if contacts is not None:
                print(f"Found {len(contacts)} contacts in database")
                if len(contacts) > 0:
                    print("Sample contact:")
                    print(contacts.iloc[0])
            else:
                print("No contacts found or error occurred")
        else:
            print("Database connection test failed")
    except Exception as e:
        print(f"Error testing database: {e}")
    finally:
        db_manager.disconnect() 