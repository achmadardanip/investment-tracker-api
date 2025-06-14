# **Investment Tracker API**

This project started as a simple REST API. Version 2 introduces multi-currency investments, real-time WebSocket updates, background task processing with Celery and a GraphQL API layer.
Version 3 adds experimental features such as on-chain settlements, machine learning based fraud detection, transaction reconciliation, a P2P matching engine and delegated yield strategies.

## Version 2 Branch

The `version-2` branch contains the latest updates with multi-currency support,
WebSockets, Celery tasks and GraphQL APIs. Use this branch for submission and
future development.

## **Project Structure**

investment-tracker-api/  
├── manage.py  
├── requirements.txt  
├── README.md  
├── config/  
│   ├── \_\_init\_\_.py  
│   ├── asgi.py  
│   ├── settings.py  
│   ├── urls.py  
│   └── wsgi.py  
├── apps/  
│   ├── \_\_init\_\_.py  
│   ├── investments/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── admin.py  
│   │   ├── apps.py  
│   │   ├── migrations/  
│   │   ├── models.py  
│   │   ├── serializers.py  
│   │   ├── services.py  
│   │   ├── urls.py  
│   │   └── views.py  
└── fixtures/  
    └── sample\_data.json

## **Setup Instructions**

1. **Clone this repository:**
```
git clone https://github.com/achmadardanip/investment-tracker-api.git  
cd investment-tracker-api
```

2. **Create a virtual environment and activate it:**  
```
python -m venv venv  
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. **Install the required dependencies:**  
```
pip install -r requirements.txt
```

4. **Create database migrations for the investments app:**  
```
python manage.py makemigrations investments
```

5. **Apply database migrations to create the tables:**  
```
python manage.py migrate
```

6. **Load sample data (Optional):**  
```
python manage.py loaddata fixtures/sample_data.json
```

This command will create a superuser (admin) with the password adminpassword and some sample investment and transaction data.  

7. **Run the development server:**  
```
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/.



## **API Endpoints**

The base URL for the API is /api/v1/.

### GraphQL

An experimental GraphQL endpoint is available at `/graphql/`.

### **Authentication**

This API uses JWT for authentication. To access protected endpoints, you need to obtain a token and include it in the Authorization header as a Bearer token.

* **POST** /api/token/  
  * Get a JWT token by providing a username and password.  
* **POST** /api/token/refresh/  
  * Refresh an expired JWT token using a refresh token.

### **Investments**

* **GET** /api/v1/investments/  
  * **Description:** Retrieves a paginated list of all investments for the authenticated user, ordered by purchase date (newest first).  
  * **Header:** Authorization: Bearer \<your\_access\_token\>  
  * **Response:**  
    ```
    {  
        "count": 2,  
        "next": null,  
        "previous": null,  
        "results": [  
            {  
                "id": 1,  
                "asset_name": "Tesla Stocks",  
                "amount_invested": "10000.00",  
                "purchase_date": "2025-06-01T12:00:00Z",  
                "current_value": "12000.00",  
                "is_active": true,  
                "profit_loss": "2000.00",  
                "profit_loss_percentage": "20.00"  
            }  
        ]  
    }
    ```

* **POST** /api/v1/investments/  
  * **Description:** Creates a new investment for the authenticated user. A corresponding 'PURCHASE' transaction log is created automatically.  
  * **Header:** Authorization: Bearer \<your\_access\_token\>  
  * **Body:**  
    ```
    {  
        "asset_name": "Apple Stocks",  
        "amount_invested": "5000.00",  
        "current_value": "5100.00",  
        "purchase_date": "2025-06-08T10:00:00Z"  
    }
    ```

  * **Validation:** amount_invested must be at least $1000.  
  * **Response (201 Created):** The newly created investment object.  
* **GET** /api/v1/investments/summary/  
  * **Description:** Provides an aggregated summary of the user's investment portfolio.  
  * **Header:** Authorization: Bearer \<your\_access\_token\>  
  * **Response:**
  ```
    {  
        "total_invested": "35000.00",  
        "current_portfolio_value": "36000.00",  
        "total_profit_loss": "1000.00",  
        "overall_roi_percentage": "2.86",  
        "active_investments_count": 2,  
        "best_performing_investment": { "...best investment data..." },  
        "worst_performing_investment": { "...worst investment data..." },  
        "insights": {  
            "average_holding_period_days": 270.5,  
            "preferred_investment_size": 17500.00  
        }  
    }
  ```

## **Database**

This project uses **SQLite** for simplicity and ease of setup, as specified in the assignment requirements. No external database server is needed.

## **Sample curl Commands**

1. **Get Token:**  
   **Windows (Command Prompt / PowerShell):**
   ``` 
   curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"youradminpassword\"}"
   ```
   Example:
   
   ![WhatsApp Image 2025-06-08 at 09 26 06_ecd3ec15](https://github.com/user-attachments/assets/35f94c39-23a8-47bc-a703-1651076c3349)


   **macOS / Linux (Bash / Zsh):**
   ```  
   curl \-X POST http://127.0.0.1:8000/api/token/ \-H "Content-Type: application/json" \-d '{"username": "admin", "password": "yournewpassword"}'
   ```

2. **List Investments:**
   ```  
   curl -X GET http://127.0.0.1:8000/api/v1/investments/ -H "Authorization: Bearer <yourtoken>"
   ```
   Example:
   
   ![WhatsApp Image 2025-06-08 at 09 27 59_804f078d](https://github.com/user-attachments/assets/c6af7346-9a0d-4c43-8e7d-37d8adfdfc37)


3. **Create Investment:**  
   **Windows (Command Prompt / PowerShell):**
   ```  
   curl -X POST http://127.0.0.1:8000/api/v1/investments/ -H "Content-Type: application/json" -H "Authorization: yourtoken" -d "{\"asset_name\": \"yourassetname\", \"amount_invested\": \"youramountinvested\", \"current_value\": \"yourcurrentvalue\", \"purchase_date\": \"yourpurchasedate\"}"
   ```
   Example:
   
   Validation Failed:
   
   ![WhatsApp Image 2025-06-08 at 09 27 25_3ba23d15](https://github.com/user-attachments/assets/0417a7c9-0bf5-4529-ac6d-24494f978098)

   Validation Success:

   ![WhatsApp Image 2025-06-08 at 09 28 41_76945239](https://github.com/user-attachments/assets/78086c54-e180-4afb-bd09-2a7ea47b3687)

   

   

   **macOS / Linux (Bash / Zsh):**
   ```  
   curl \-X POST http://127.0.0.1:8000/api/v1/investments/ \-H "Content-Type: application/json" \-H "Authorization: Bearer \<your\_access\_token\>" \-d '{"asset\_name": "New Tech Fund", "amount\_invested": "2500", "current\_value": "2500", "purchase\_date": "2025-06-08T10:00:00Z"}'
   ```

4. **Get Summary:**
   ```  
   curl -X GET http://127.0.0.1:8000/api/v1/investments/ -H "Authorization: Bearer yourtoken"
   ```
   Example:

   ![image](https://github.com/user-attachments/assets/098cc30a-e0b8-455c-9ec0-e158ed65c6a5)


## **Assumptions Made**

* The current_value of an investment is provided by the user upon creation and can be updated via the Django admin or a future PATCH endpoint (not included in this test).  
* The is_active flag is True by default for new investments.  
* Profit/loss calculations are based on the simple formula: current_value - amount_invested.  
* The reference_id for transactions is a unique UUID generated automatically upon creation.

## **Troubleshooting**

### **Error: "No active account found with the given credentials"**

If you get this error when trying to obtain a token, it means the password you provided does not match the one in the database. You can reset the password for the admin user by running the following command and following the prompts:
```
python manage.py changepassword admin
```

After you set the new password, use it in the curl command to get the token.
A Postman collection `InvestmentTracker.postman_collection.json` is included with sample requests for all endpoints.
