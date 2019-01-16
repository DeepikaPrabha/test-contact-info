# test-contact-info
* App for saving contacts
* It uses python flask to build up api and postgresql to save contact
* It is deployed in heroku web app.
* https://test-contact-info.herokuapp.com

## Endpoints

### Add user
* url = https://test-contact-info.herokuapp.com/add_user
* HTTP Request type = POST
* Request param : [name, email, city] (All required)

### Update user
* https://test-contact-info.herokuapp.com/update_user
* HTTP Request type = PUT
* Request param : email - (required) , [name, city] - optional

### Delete User
* https://test-contact-info.herokuapp.com/delete_user
* HTTP Request type = Delete
* Request param : email - (required)

### Search by name
* https://test-contact-info.herokuapp.com/search_by_name
* HTTP Request type = GET
* Request param : name - (required)

### Search by email
* https://test-contact-info.herokuapp.com/search_by_email
* HTTP Request type = GET
* Request param : email - (required)

## Notes
* It needs basic authentication to use ADD/UPDATE/DElETE endpoint
* For searching, it doesn't require any login credentials