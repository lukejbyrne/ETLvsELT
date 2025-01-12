# ETL vs ELT: A Comparison of Data Processing Methodologies

Welcome to the **ETL vs ELT** repository! This project demonstrates the differences between the two popular data processing methodologies: **Extract, Transform, Load (ETL)** and **Extract, Load, Transform (ELT)**. It includes two Python scripts, `etl_process.py` and `elt_process.py`, showcasing how to process earthquake data using each approach.

---

## 🛠️ **Project Overview**

### 1. **ETL (Extract, Transform, Load)**  
   - **Process**: Data is **extracted** from the source, **transformed** to meet target requirements, and then **loaded** into the target storage.
   - **Key Feature**: Transformation occurs *before* data is loaded into the destination.
   - **Use Case**: Traditional systems like data warehouses, where data needs to be structured and cleaned before loading.

### 2. **ELT (Extract, Load, Transform)**  
   - **Process**: Data is **extracted** from the source, **loaded** into the target storage in its raw form, and then **transformed** within the storage system.
   - **Key Feature**: Transformation happens *after* data is loaded.
   - **Use Case**: Modern systems like cloud data lakes, where raw data is stored for flexibility and transformations are performed as needed.

---

## 📂 **Repository Structure**

```
/repo-root
│
├── etl_process.py   # Demonstrates the ETL methodology
├── elt_process.py   # Demonstrates the ELT methodology
├── requirements.txt # Python dependencies
├── README.md        # Project documentation
```

---

## 🚀 **Getting Started**

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

### 2. **Set Up the Environment**
1. **Create a Virtual Environment**  
   Create a new Python virtual environment to isolate dependencies:
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**  
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**  
   Install the required libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**  
   Ensure all dependencies are installed correctly:
   ```bash
   pip list
   ```

5. **Run the Scripts**  
   - For the ETL process:
     ```bash
     python etl_process.py
     ```
   - For the ELT process:
     ```bash
     python elt_process.py
     ```

### 3. **Run the Scripts**

#### ETL Process
```bash
python etl_process.py
```
- Fetches earthquake data from the USGS API.
- Performs transformations locally.
- Saves the cleaned data into "Silver" and "Gold" layers.

#### ELT Process
```bash
python elt_process.py
```
- Fetches earthquake data from the USGS API.
- Loads raw data into the "Bronze" and "Silver" layers.
- Applies transformations in the "Gold" layer.

---

## 📊 **Key Differences Between ETL and ELT**

| **Aspect**         | **ETL**                                   | **ELT**                                 |
|---------------------|-------------------------------------------|-----------------------------------------|
| **Transformation** | Before loading data into storage.         | After loading data into storage.        |
| **Performance**    | Suitable for smaller datasets.            | Leverages modern storage and processing power for big data. |
| **Flexibility**    | Requires schema upfront for transformations. | Stores raw data for on-demand transformations. |
| **Use Case**       | Data warehouses, legacy systems.          | Data lakes, modern cloud architectures. |

---

## 📚 **Dependencies**

This project requires the following Python libraries:

- `requests` - For fetching data from the USGS API.
- `pandas` - For data manipulation and transformation.
- `geopy` - For reverse geocoding latitude/longitude to country codes.

Install them using:
```bash
pip install -r requirements.txt
```

---

## 👨‍💻 **Contributing**

Contributions are welcome! If you'd like to improve this project or add additional examples, feel free to submit a pull request.


---

## 🏗️ **Future Enhancements**

- Add support for additional data sources.
- Compare performance metrics for large-scale data.
- Provide cloud-based implementations using AWS, Azure, or GCP.

---

### 🔗 **Connect with Me**

If you found this project helpful or have any questions, feel free to reach out on [LinkedIn](https://www.linkedin.com/in/lukejbyrne).