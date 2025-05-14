#!/usr/bin/env python3
"""
MongoDB Viewer - A simple GUI to view MongoDB databases and collections
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from pymongo import MongoClient
from bson import json_util

class MongoDBViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("MongoDB Viewer")
        self.root.geometry("800x600")
        
        # MongoDB connection
        self.client = None
        self.current_db = None
        self.current_collection = None
        
        # Create the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Connection frame
        self.connection_frame = ttk.LabelFrame(self.main_frame, text="MongoDB Connection", padding="10")
        self.connection_frame.pack(fill=tk.X, pady=5)
        
        # Connection string
        ttk.Label(self.connection_frame, text="Connection String:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.connection_string = tk.StringVar(value="mongodb://localhost:27017/")
        ttk.Entry(self.connection_frame, textvariable=self.connection_string, width=50).grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.connection_frame, text="Connect", command=self.connect_to_mongodb).grid(row=0, column=2, padx=5, pady=5)
        
        # Database and collection selection
        self.selection_frame = ttk.Frame(self.main_frame)
        self.selection_frame.pack(fill=tk.X, pady=5)
        
        # Database selection
        ttk.Label(self.selection_frame, text="Database:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.database_var = tk.StringVar()
        self.database_combo = ttk.Combobox(self.selection_frame, textvariable=self.database_var, state="readonly", width=30)
        self.database_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.database_combo.bind("<<ComboboxSelected>>", self.on_database_selected)
        
        # Collection selection
        ttk.Label(self.selection_frame, text="Collection:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.collection_var = tk.StringVar()
        self.collection_combo = ttk.Combobox(self.selection_frame, textvariable=self.collection_var, state="readonly", width=30)
        self.collection_combo.grid(row=0, column=3, sticky=tk.W, pady=5)
        self.collection_combo.bind("<<ComboboxSelected>>", self.on_collection_selected)
        
        # View button
        ttk.Button(self.selection_frame, text="View Data", command=self.view_data).grid(row=0, column=4, padx=5, pady=5)
        
        # Data display
        self.data_frame = ttk.LabelFrame(self.main_frame, text="Data", padding="10")
        self.data_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text area for data display
        self.data_text = scrolledtext.ScrolledText(self.data_frame, wrap=tk.WORD, width=80, height=20)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Not connected")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Try to connect on startup
        self.connect_to_mongodb()
    
    def connect_to_mongodb(self):
        """Connect to MongoDB using the provided connection string"""
        try:
            connection_string = self.connection_string.get()
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ismaster')
            
            # Update status
            self.status_var.set(f"Connected to MongoDB at {connection_string}")
            
            # Update database list
            self.update_database_list()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to MongoDB: {str(e)}")
            self.status_var.set(f"Connection failed: {str(e)}")
    
    def update_database_list(self):
        """Update the list of databases"""
        if self.client:
            try:
                databases = self.client.list_database_names()
                self.database_combo['values'] = databases
                
                if databases:
                    self.database_combo.current(0)
                    self.on_database_selected(None)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get database list: {str(e)}")
    
    def on_database_selected(self, event):
        """Handle database selection"""
        if self.client:
            db_name = self.database_var.get()
            if db_name:
                self.current_db = self.client[db_name]
                self.update_collection_list()
    
    def update_collection_list(self):
        """Update the list of collections for the selected database"""
        if self.current_db:
            try:
                collections = self.current_db.list_collection_names()
                self.collection_combo['values'] = collections
                
                if collections:
                    self.collection_combo.current(0)
                    self.on_collection_selected(None)
                else:
                    self.collection_var.set("")
                    self.data_text.delete(1.0, tk.END)
                    self.data_text.insert(tk.END, f"No collections found in database '{self.current_db.name}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get collection list: {str(e)}")
    
    def on_collection_selected(self, event):
        """Handle collection selection"""
        if self.current_db:
            collection_name = self.collection_var.get()
            if collection_name:
                self.current_collection = self.current_db[collection_name]
    
    def view_data(self):
        """View data from the selected collection"""
        if self.current_collection:
            try:
                # Clear the text area
                self.data_text.delete(1.0, tk.END)
                
                # Get document count
                count = self.current_collection.count_documents({})
                self.data_text.insert(tk.END, f"Collection: {self.current_collection.name}\n")
                self.data_text.insert(tk.END, f"Documents: {count}\n\n")
                
                # Get the first 10 documents
                documents = list(self.current_collection.find().limit(10))
                
                if documents:
                    for i, doc in enumerate(documents):
                        # Convert MongoDB document to JSON
                        doc_json = json_util.loads(json_util.dumps(doc))
                        
                        # Format the document
                        self.data_text.insert(tk.END, f"Document {i+1}:\n")
                        for key, value in doc_json.items():
                            self.data_text.insert(tk.END, f"  {key}: {value}\n")
                        self.data_text.insert(tk.END, "\n")
                    
                    if count > 10:
                        self.data_text.insert(tk.END, f"... and {count - 10} more documents\n")
                else:
                    self.data_text.insert(tk.END, "No documents found in this collection.")
                
                # Update status
                self.status_var.set(f"Viewing data from {self.current_db.name}.{self.current_collection.name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to view data: {str(e)}")
                self.data_text.delete(1.0, tk.END)
                self.data_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBViewer(root)
    root.mainloop()
