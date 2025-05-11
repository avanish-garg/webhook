import requests

# 1. Candidate details for webhook generation
NAME   = "John Doe"
REG_NO = "REG12347"
EMAIL  = "john@example.com"

# 2. final SQL solution(since I got reg odd)
FINAL_SQL_QUERY = """
SELECT 
    p.AMOUNT AS SALARY,
    e.FIRST_NAME || ' ' || e.LAST_NAME AS NAME,
    (EXTRACT(YEAR FROM p.PAYMENT_TIME) - EXTRACT(YEAR FROM e.DOB))
      - CASE
          WHEN (EXTRACT(MONTH FROM e.DOB) > EXTRACT(MONTH FROM p.PAYMENT_TIME))
            OR (EXTRACT(MONTH FROM e.DOB) = EXTRACT(MONTH FROM p.PAYMENT_TIME)
                AND EXTRACT(DAY FROM e.DOB) > EXTRACT(DAY FROM p.PAYMENT_TIME))
          THEN 1 ELSE 0
        END AS AGE,
    d.DEPARTMENT_NAME
FROM 
    PAYMENTS p
JOIN 
    EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    EXTRACT(DAY FROM p.PAYMENT_TIME) <> 1
  AND p.AMOUNT = (
        SELECT MAX(AMOUNT)
        FROM PAYMENTS
        WHERE EXTRACT(DAY FROM PAYMENT_TIME) <> 1
    );
""".strip()

def generate_webhook(name, reg_no, email):
    """Step 1: Register and get webhook URL + access token"""  
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {"name": name, "regNo": reg_no, "email": email}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["webhook"], data["accessToken"] 

def submit_solution(webhook_url, token, sql_query):
    """Step 2: Submit your SQL using the token in Authorization header"""  
    headers = {
        "Authorization": token,            
        "Content-Type": "application/json"
    }
    payload = {"finalQuery": sql_query}
    resp = requests.post(webhook_url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    # Generate
    webhook_url, access_token = generate_webhook(NAME, REG_NO, EMAIL)
    print("🔗 Webhook URL: ", webhook_url)
    print("🔑 Access Token:", access_token)

    # Submit
    result = submit_solution(webhook_url, access_token, FINAL_SQL_QUERY)
    print("✅ Submission response:", result)

if __name__ == "__main__":
    main()
