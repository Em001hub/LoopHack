#!/bin/bash
psql -U postgres loophack -f database/seeds/dev/users.sql
