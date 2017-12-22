# Lab 2

### Topic 
Collecting of distributed data

### Prerequisites

- VCS(Version Control System) Git
- Knowledge about transport protocols
- Basic knowledge of distributed system
- Json, Xml
- Validation of semi-structured data

### Objectives

- Use udp protocol to send unicast and multicast
- Use tcp protocol to send data from nodes
- Process of data from collection of objects
- Developing of a mediator to facilitate data aggregation from nodes
- Implement a module to validate json, xml 

### Representation of the System

![Representation of the System](./docs/pad-lab-2.png)

### Instruction to run project
- Clone repo
- Start nodes one by one and give each one a unique port address
- Start Mediator 
- Start Client

```
python Node.py 5001
python Node.py 5002
python Node.py 5003
python Mediator.py
python Client.py
```



