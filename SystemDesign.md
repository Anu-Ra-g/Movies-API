# System Design of the API

The application houses metadata for 5 million movies and is currently handling 15 million requests, from both anonymous and authenticated users. 

To scale this system, so that it could accomodate 5 times its current userbase, I'd see over these things. 

1. First, I'd go over the current architure of the system and identify where the potential bottlenecks could occur. 

2. The previous system uses a single server for handling requests and responses. Considering the current usage of the customers, I'd go for a microservice architecture, each responsible for specific funtionalities, such movie data retireval, user authentication and user management. 

3. Containerize each microservice using technologies like Docker and orchestrate them using a container orchestration platform like Kubernetes. This allows for easy scaling, deployment, and management of services. Configure autoscaling for microservices based on metrics like CPU utilization, request rates, or latency.

3. Then I'd use a load balancer like NGNIX, HAProxy to distribute incoming API requests across multiple instances of each microservice. The load balancer will be deployed as dedicated infrastructure component.

4. Then I'll implement a caching layer to store frequently accessed data, such as movie metadata, to reduce the load on the database and improve response times. Increase the cache size and use a distributed caching system like Redis or Memcached to handle the increased load.

5. After that, I'll review the current database system. Use a distributed database system (e.g., Apache Cassandra, Amazon DynamoDB, or Google Cloud Bigtable) to horizontally scale the data storage and implement database sharding to distribute data across multiple servers.

6. Use a Content Delivery Network (CDN) for serving static content and implement rate limiting to protect against abuse and potential DDoS attacks. 