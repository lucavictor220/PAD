Example of Send Message
```
{
    'type': 'send',
    'topic': 'RED',
    'payload': 'message to be send'
}
```

Example of a Get message:
```
{
    'type': 'get',
    'topic': 'RED',
    'payload': ''
}
```

Message broker send back messages of acknowledgement:
```
{
    'type': 'ok',
    'payload': 'Message added to RED queue'
}
```

In case of an error:

```
{
    'type': 'error',
    'payload': 'No such topic'
}
```