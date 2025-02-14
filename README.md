# HTTP-DDS Bridge Proof-of-Concept

## Members: Ashutosh Mane, Jaabir Ahamed Saleem, Dennis Shih

### Project Description:  
This project tackles the  challenge of data exchange within Mainspring Energy's (MSE) infrastructure.  Currently, data sharing between devices (cloud infrastructure, servers, embedded systems, etc.) is done through a series of hardware platforms, programming languages, and data serialization methods.  This often leads to a tedious and error-prone process of manually coding data conversions, which may lead to inefficiencies and vulnerability during production.  This proof-of-concept project aims to improve this process by developing an HTTP-to-DDS bridge.  This bridge will act as a data translator, converting HTTP requests (which is commonly used for web-based applications) into DDS (Data Distribution Service) format.

The primary technical approach of this project is the use of an Interface Definition Language (IDL) to implement automated code generation.  By defining the data structures in a standardized IDL, we can automatically generate the code necessary to perform the data transformations between JSON (used in HTTP) and the specific data types used by DDS. This proof-of-concept would eliminate the need for manual coding, reducing development time and minimizing the risk of introducing bugs from human error. This solution will ensure consistency and simplify maintenance, as changes to data structures only require updates to the IDL, and then the regeneration of the code. 
