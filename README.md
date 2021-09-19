# mann-backend


# to-do
- request and response from android application
- draft post/ published post to included

# to-do completed
- removed the cyclic dependency from signals.
- included the permissions in cred ?? only owner edit with minimal code
- authentication-done
- 

# sample mutation query
```
mutation{
  relayCreatePost(input:{
    title:"Testing Authorization and Authentiation",
    content:"This is a test",
    tags:"test"
  }){
    post {
      id
      user{
          username
      }
      
      content
    }
  }
}
```
