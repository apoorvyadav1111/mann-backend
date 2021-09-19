# mann-backend-graphql
to get revert back version using requirements.txt and git

# to-do
# remove the cyclic dependency from signaks --done
# include the permissions in cred ?? only owner edit with minimal code

# authentication is completed for now 


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