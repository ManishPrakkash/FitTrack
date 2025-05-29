#!/usr/bin/env python3
"""
MongoDB Connection Test Script for FitTrack
This script tests various MongoDB connection configurations to diagnose timeout issues.
"""

import os
import sys
import time
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connection strings to test
CONNECTION_STRINGS = [
    # Original connection string
    'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db',
    
    # With specific database
    'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/fittrack_db?retryWrites=true&w=majority&appName=fitrack-db',
    
    # With timeout settings
    'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&socketTimeoutMS=10000',
    
    # With SSL settings
    'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db&ssl=true&ssl_cert_reqs=CERT_NONE',
]

def test_connection(uri, test_name):
    """Test a MongoDB connection string."""
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"URI: {uri[:50]}...")
    print(f"{'='*60}")
    
    try:
        # Create client with shorter timeout for testing
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=10000,  # 10 seconds
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            maxPoolSize=1
        )
        
        print("✓ Client created successfully")
        
        # Test server selection
        start_time = time.time()
        server_info = client.server_info()
        connection_time = time.time() - start_time
        
        print(f"✓ Connected successfully in {connection_time:.2f} seconds")
        print(f"✓ MongoDB version: {server_info.get('version', 'Unknown')}")
        
        # Test database access
        db = client['fittrack_db']
        collections = db.list_collection_names()
        print(f"✓ Database accessible, collections: {collections}")
        
        # Test a simple operation
        test_collection = db['connection_test']
        test_doc = {'test': True, 'timestamp': time.time()}
        result = test_collection.insert_one(test_doc)
        print(f"✓ Write test successful, inserted ID: {result.inserted_id}")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("✓ Cleanup successful")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError as e:
        print(f"✗ Server selection timeout: {e}")
        return False
    except ConnectionFailure as e:
        print(f"✗ Connection failure: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_dns_resolution():
    """Test DNS resolution for MongoDB Atlas cluster."""
    print(f"\n{'='*60}")
    print("Testing DNS Resolution")
    print(f"{'='*60}")
    
    import socket
    
    hostnames = [
        'fitrack-db.9hmlhdb.mongodb.net',
        'ac-pc8vzlb-shard-00-00.9hmlhdb.mongodb.net',
        'ac-pc8vzlb-shard-00-01.9hmlhdb.mongodb.net',
        'ac-pc8vzlb-shard-00-02.9hmlhdb.mongodb.net'
    ]
    
    for hostname in hostnames:
        try:
            ip = socket.gethostbyname(hostname)
            print(f"✓ {hostname} -> {ip}")
        except socket.gaierror as e:
            print(f"✗ {hostname} -> DNS resolution failed: {e}")

def test_network_connectivity():
    """Test network connectivity to MongoDB Atlas."""
    print(f"\n{'='*60}")
    print("Testing Network Connectivity")
    print(f"{'='*60}")
    
    import socket
    
    hosts = [
        ('ac-pc8vzlb-shard-00-00.9hmlhdb.mongodb.net', 27017),
        ('ac-pc8vzlb-shard-00-01.9hmlhdb.mongodb.net', 27017),
        ('ac-pc8vzlb-shard-00-02.9hmlhdb.mongodb.net', 27017)
    ]
    
    for host, port in hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✓ {host}:{port} - Connection successful")
            else:
                print(f"✗ {host}:{port} - Connection failed (error code: {result})")
        except Exception as e:
            print(f"✗ {host}:{port} - Error: {e}")

def main():
    """Main test function."""
    print("MongoDB Connection Diagnostic Tool")
    print("=" * 60)
    
    # Test DNS resolution
    test_dns_resolution()
    
    # Test network connectivity
    test_network_connectivity()
    
    # Test different connection strings
    successful_connections = 0
    
    for i, uri in enumerate(CONNECTION_STRINGS, 1):
        if test_connection(uri, f"Test {i}"):
            successful_connections += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Successful connections: {successful_connections}/{len(CONNECTION_STRINGS)}")
    
    if successful_connections == 0:
        print("\n❌ All connection attempts failed!")
        print("\nPossible issues:")
        print("1. Network connectivity problems")
        print("2. Firewall blocking MongoDB ports")
        print("3. MongoDB Atlas IP whitelist restrictions")
        print("4. Incorrect credentials")
        print("5. MongoDB Atlas cluster is down")
        
        print("\nRecommended actions:")
        print("1. Check your internet connection")
        print("2. Verify MongoDB Atlas IP whitelist includes your IP")
        print("3. Confirm cluster is running in MongoDB Atlas dashboard")
        print("4. Try connecting from a different network")
    else:
        print(f"\n✅ {successful_connections} connection(s) successful!")

if __name__ == "__main__":
    main()
