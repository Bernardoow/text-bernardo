# Thoughts

## Text Handler

### Structure

1. It should be a class
2. It should receive in the init by param one array of text
3. it should has four mothod one of kind of operation
    * return the list of single words
    * return the quantity of occorence of each word
    * return the list of tuple(2th) words
    * return the quantity of ocorrence of tuple(2th) words
4. it should process the text when some of method will be call. (Ex if call list of single words JUST process the single words it won't do the process of list of tuple)

### One word 

1. it should ignore case and punctuation
2. it should keep just one entry of each word
3. it should fit together every text inside of system to create list with every valid word
4. it should calculate the quantity of occorrence of the each word(in list of item#3) for each text
5. it should remove stop-words

Example: [falar, é, facil, mostre]

### two word 

1. it should ignore case and punctuation
2. it should keep just one entry of each (tuple(2elements) word)
3. it should fit together every text inside of system to create list with every valid word
4. it should calculate the quantity of occorrence of the each word(in list of item#3) for each text
5. it should remove stop-words

Example: [(falar, é,), (é, fácil), (facil, mostre)]


## API REST

Must be a simple flask app. 

### Libs
    *. Using lib sqlalchemy and migrate to handle database.
    *. Lib RESTPlus’s to handler api rest.
    *. Lib Mashmallow to handle with encode and decode data.

### Endpoints

1. api/v1/send-text 
    Accepts only post with payload with one variable text

2. api/v1/isoleted-vocabulary
    Accept only get to get vocabulary

3. api/v1/2thgram-vocabulary
    Accept only get to get vocabulary

4. api/v1/isoleted-vectors
    Accept only get to get vectors 

5. api/v1/2thgram-vectors
    Accept only get to get vectors 

6. api/v1/delete-text/<int:textId>
    accept only delete. (Maybe I will do this if I have time to build frontend side)
