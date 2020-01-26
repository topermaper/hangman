# Project Title
This is a simple classic hangout webgame
## Getting Started
Clone the repository
```bash
git clone https://github.com/topermaper/hangman.git
```

Create virtual env and activate
```bash
virtualenv -p /usr/bin/python3.6 myenv
. myenv/bin/activate
```

Install requeriments file
```bash
pip3 install -r requirements.txt
```

Run app
```bash
 python run.py
```

## Usage
The app home page is: "http://localhost:5000/", open it in the browser.
Rules are standard. You lose after 5 misses.

### API
API in "http://localhost:5000/api/v1"

#### Implemented actions:
######  Create new user
POST /api/v1/users
Post a JSON with name and email. It returns the resource location in the response header.

###### Get user
GET /api/v1/users/id
Needs authentication
###### Generate auth token
GET /api/v1/token
Needs the header Authorization to be set with the user credentials.

Example:
For user marcos6340@gmail.com:test123 the header Authorization will be set as follows:
`Authorization:Basic bWFyY29zNjM0MEBnbWFpbC5jb206dGVzdDEyMw==`

response:
`{
  "duration": 3600,
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MDA3MDUwNCwiZXhwIjoxNTgwMDc0MTA0fQ.eyJpZCI6NH0.rRh7AcNBF5fKVwkyaVcHVqfXH__mJBR1_388V7mVM-97yOfG5wF9Xb5UxS3Ftaax24Vg2h5wdc_OdjDdth7Zjw"
}`

To authenticate using the token concatenate token + 'unused', encoded base 64 and add to the header Authorization for all the requests needing authentication.

`
eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MDA3MDk5NywiZXhwIjoxNTgwMDc0NTk3fQ.eyJpZCI6Mzh9.8OBII0Pa5xh8wBjAbUkexb5QFhN_qadbrGH3vZgeENkwMB9PVn7vv7CjiMmKAXaIFWYByP-AU9PLK2bFaWJgWg:unused`

will set header as follows:
`Authorization: Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UVTRNREEzTURrNU55d2laWGh3SWpveE5UZ3dNRGMwTlRrM2ZRLmV5SnBaQ0k2TXpoOS44T0JJSTBQYTV4aDh3QmpBYlVrZXhiNVFGaE5fcWFkYnJHSDN2WmdlRU5rd01COVBWbjd2djdDamlNbUtBWGFJRldZQnlQLUFVOVBMSzJiRmFXSmdXZzp1bnVzZWQ=`

###### Create new game
POST /api/v1/games

This does not required parameters, just sent the authentication header

###### Get game
GET /api/v1/users/games/id
Needs authentication
###### User attempts to guess the word
PATCH /api/v1/users/games/id

Send a json with the list of all user guesses. You have to send the previous list plus the latest guess. Otherwise patch request won't be successful.
`
{
    "user_guess": [
    "s","o","r","d","a","e","1"
  ]
}
`
## Author
* **Marcos Edo**

