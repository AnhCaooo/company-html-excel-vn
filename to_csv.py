import pandas as pd 

def main():
    # reading the text file which is generated from main.py 
    # and creating dataframe 
    dataframe = pd.read_csv("company_info.txt", dtype=str) 
    
    # storing this dataframe in a csv file 
    dataframe.to_csv('company_info.csv',  
                    index = None) 
    
    print('convert text file to csv successfully')
    

if __name__ == "__main__":
    main() 