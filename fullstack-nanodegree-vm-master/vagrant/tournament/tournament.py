#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def query_helper(statement, params=None):
    """Method to run queries."""
    conn = connect()
    cur = conn.cursor()
    cur.execute(statement, params)
    conn.commit()
    conn.close()


def single_query_helper(statement, params=None):
    """Method to run queries with one result."""
    conn = connect()
    cur = conn.cursor()
    cur.execute(statement, params)
    result = cur.fetchone()[0]
    conn.close()
    return result


def multiple_queries_helper(statement, params=None):
    """Method to run queries with multiple columns."""
    conn = connect()
    cur = conn.cursor()
    cur.execute(statement, params)
    results = cur.fetchall()
    conn.close()
    return results


def swiss_pairings_helper(statement, params=None):
    """Method to run swiss pairings query."""
    conn = connect()
    cur = conn.cursor()
    cur.execute(statement, params)
    result = cur.fetchall()
    pairings = []
    for index, player in enumerate(result):
        if index % 2 == 0:
            pair = (
                player[0], player[1],
                result[index + 1][0], result[index + 1][1])
            pairings.append(pair)
    conn.close()
    return pairings


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    query_helper("DELETE FROM matches")


def deletePlayers():
    """Remove all the player records from the database."""
    query_helper("DELETE FROM players")


def countPlayers():
    """Returns the number of players currently registered."""
    return single_query_helper("SELECT COUNT(*) FROM players")


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    query_helper("INSERT INTO players (name) VALUES (%s)", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return multiple_queries_helper(
        """
        SELECT players.player_id, players.name,
            (SELECT count(matches.winner)
            FROM matches
            WHERE players.player_id = matches.winner) AS wins,
            (SELECT count(matches.match_id)
            FROM matches
            WHERE players.player_id = matches.winner
            OR players.player_id = matches.loser) AS matches
        FROM players
        ORDER BY wins DESC, matches DESC
        """
    )


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query_helper("INSERT INTO matches (winner, loser) VALUES (%s, %s)",
                (winner, loser,))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    return swiss_pairings_helper(
        """
        SELECT players.player_id, players.name,
            (SELECT count(matches.winner)
            FROM matches
            WHERE players.player_id = matches.winner) AS wins
        FROM players LEFT JOIN matches
        ON players.player_id = matches.winner
        OR players.player_id = matches.loser
        GROUP BY players.player_id
        ORDER BY wins DESC
        """
    )
