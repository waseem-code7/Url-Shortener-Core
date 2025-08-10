# URL-SHORTENER-CORE

This server is responsible for creating, updating, and deleting short URLs. It integrates with Zookeeper, which assigns a range of numbers using ephemeral nodes. These ranges are then used to generate short URL IDs using Base62 encoding.

---

## Prerequisites to Start the Server  
1. Ensure Docker is installed.  
2. Run the Redpanda Docker Compose file from the **Url-Shortener-Core** repository to start a Kafka server in cluster mode.  
3. Start a Redis server in cluster mode.  
4. Start Zookeeper.  
5. Set up DynamoDB — follow the instructions below.  
6. Update the environment variables accordingly.

---

## Creating DynamoDB Tables

Create the following tables in DynamoDB:

### 1. URL_DATA  
- **Partition Key**: `short_url_id`

### 2. USER_DATA  
- **Partition Key**: `email`

---

## Steps to Install  
1. Clone the repository.  
2. Navigate to the repository folder:  
   ```bash
   cd Url-Shortener-Core
   pip install -r requirements.txt
   uvicorn main:app --reload

