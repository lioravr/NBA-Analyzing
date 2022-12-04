# NBA Standing All Over The Years

## Features

---

**Update**
The project doesn't run for now. 
The sloution for the problem is to add "" in a new line at the requirements in the backend file. 


1. Explore all the players from the begining of the league until today.

2. Filter by years, position and player stat.

3. Analyse the scoring plot by years.

* Notice: all the data are taken from <https://www.basketball-reference.com/>


## Review

https://youtu.be/3UiJPcndv-8

## Get Started

---

1. Download all the files and zip them.

2. open WSL and navigate to the project path

3. Run this command on your WSL

    ```CMD
    docker-compose build
    docker-compose up -d
    ```

4. go to [this link](http://localhost:8501 "")

5. To close the app please enter in terminal

    ```
    docker-compose down --rmi all 
    ```

## Requirements

* WSL (preferable version 2)
* Docker Desktop

## Built On

---

* FastAPI

* Streamlit

* Matplotlib

* Plotly
