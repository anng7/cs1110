# a1.py
# Quinn Beightol (qeb2), Mengyun Xia (mx48)
# September 16, 2012
"""Module for currency exchange

This module provides several String parsing functions to 
implement a simple currency exchange routine using an 
online currency service. The primary function in this 
module is exchange()."""

import urllib2


def before_space(s):
    """Returns: Substring of <s> up to, but not including, the first space
    
    Precondition: <s> has at least one space in it"""
    
    return s[:s.find(" ")]


def after_space(s):
    """Returns: Substring of <s> after the first space
    
    Precondition: <s> has at least one space in it"""
    
    return s[s.find(" ") + 1:]


def first_inside_quotes(s):
    """Returns: The first substring of s between two (double) quote characters
    
    A quote character is one that is inside a string, not one that delimits it.
    Often we use \" to distinguish this from ".
    
    Example: if s is "a \"B C\" D", this function returns "B C".
    Example: if s is "A \"B C\" D \"E F\" G," this function still returns "B C",
    ignoring all later substrings between double quotes.
    
    Precondition: <s> is a string with at least two (double) quote characters
    inside."""
    
    start = s.find("\"") + 1
    return s[start:s.find("\"",start)] #s.find("\"",start) finds the quote
                                    #character marking the end of the substring

def get_lhs(query):
    """Returns: The LHS value in the response to a currency query
    
    Gives a JSON response to a currency query, this returns the string inside
    quotes (\") immediately following the keyword lhds. For example, if the JSON
    is
    
        "{lhs: \"2 U.S. dollars\",rhs: \"1.629327902 Euros\",error: \"\",icc: true}"
    
    the this function returns "2 U.S. dollars" (not "\"2 U.S. dollars\""). When
    the JSON is the result of an invalid substring, this function returns an
    empty string.
    
    Precondition: <query> is the response to a currency query."""
    
    substring = query[query.find("lhs"):]
    return first_inside_quotes(substring)


def get_rhs(query):
    """ Returns: The RHS value in the response to a currency query.

    Given a JSON response to a currency query, this returns the string inside
    quotes (\") immediately following the keyword rhs. For example, if the JSON is

        "{lhs: \"2 U.S. dollars\",rhs: \"1.629327902 Euros\",error: \"\",icc: true}"

    then this function returns "1.629327902 Euros" (not "\"1.629327902 Euros\"").
    It returns the empty string if the JSON is the result of on invalid query.

    Precondition: <query> is the response to a currency query."""
    
    substring = query[query.find("rhs"):]
    return first_inside_quotes(substring)


def currency_response(amount_from,currency_from,currency_to):
    """ Returns: A JSON string that is a response to a currency query.

    A currency query converts <amount_from> money in currency <currency_from>
    to the currency <currency_to>. The response should be a string of the form

        "{lhs: \"<old-amount>\",rhs: \"<new-amount>\",error: \"\",icc: true}"

    where the values <old-amount> and <new-amount> contain the value and name
    for the original and new currencies. If the query is invalid, both
    <old-amount> and <new-amount> will be empty.

    Precondition: <amount_from> is of type float, while <currency_from> and <currency_to> are of type string"""
    
    url = 'http://cs1110.cs.cornell.edu/a1/calculator.php?q=' + `amount_from`
    url = url + currency_from.upper() + '=?' + currency_to.upper()
    return urllib2.urlopen(url).read() 


def iscurrency(currency):
    """Returns: True if <currency> is a valid (3 letter code for a) currency.

    Precondition: <currency> is a string.""" 
    
    return not currency_response(1.0,'USD',currency) == '{lhs: "",rhs: "",error: "4",icc: false}'


def exchange(amount_from, currency_from, currency_to):
    """ Returns: amount of currency received in the given exchange.

    In this exchange, the user is changing <amount_from> money in
    currency <currency_from> to the currency <currency_to>. The value returned
    is a float representing the amount in currency <currencyTo>

    Precondition: <amount_from> is a float. Both <currency_from> and
    <currency_to> are strings with valid three-letter currency codes."""
    
    return float(before_space(get_rhs(currency_response(amount_from,
                                                        currency_from,
                                                        currency_to))))

