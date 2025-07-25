import pandas as pd
import json
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO

def load_file(uploaded_file):
    filename = uploaded_file.name.lower()
    
    try:
        if filename.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        
        elif filename.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
        
        elif filename.endswith(".json"):
            data = json.load(uploaded_file)
            return pd.json_normalize(data)
        
        elif filename.endswith(".xml"):
            return parse_xml(uploaded_file)
        
        elif filename.endswith(".txt"):
            # Try reading as tab-separated or comma-separated
            try:
                return pd.read_csv(uploaded_file, sep="\t")
            except:
                return pd.read_csv(uploaded_file, sep=",")
        
        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        raise RuntimeError(f"Failed to load file: {e}")


def parse_xml(file):
    """Parse basic XML structure into a DataFrame"""
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        rows = []
        headers = []

        for child in root:
            row = {}
            for sub in child:
                row[sub.tag] = sub.text
                if sub.tag not in headers:
                    headers.append(sub.tag)
            rows.append(row)

        return pd.DataFrame(rows)

    except Exception as e:
        raise RuntimeError(f"XML parsing error: {e}")
