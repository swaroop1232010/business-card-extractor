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
            dict: Contact data or None if not found
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
    
    def search_contacts(self, search_term: str) -> Optional[pd.DataFrame]:
        """
        Search contacts by name, company, or email.
        
        Args:
            search_term (str): Search term to look for
            
        Returns:
            pandas.DataFrame: DataFrame containing matching contacts, or None if error
        """
        try:
            if not self.test_connection():
                raise Exception("Database connection failed")
            
            query = text("""
            SELECT * FROM contacts 
            WHERE name LIKE :search_term OR company LIKE :search_term OR email LIKE :search_term
            ORDER BY created_at DESC
            """)
            
            search_pattern = f"%{search_term}%"
            df = pd.read_sql(query, self.engine, params={'search_term': search_pattern})
            
            logger.info(f"Found {len(df)} contacts matching '{search_term}'")
            return df
            
        except Exception as e:
            logger.error(f"Error searching contacts in database: {e}")
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