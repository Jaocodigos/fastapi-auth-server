# Introduction

This is basically a Oauth 2.0 Authorization Server, written with FastAPI.

For now, the server can handle only with **authorization_code** grant_type and has support only for S256 hash method.
There are too much to implement, but the flow is already working, so it's ok.

## Roadmap

- Add OpenID layer for authentication
- Add more options for client creation(roles, expiration time, etc)
- Make state/nonce work 
- Write tests and pipeline
- Document all content and workflow
- Add Dockerfile(please man)
- Add a relational database like MySQL or PostgreSQL(probably the last thing a will do)