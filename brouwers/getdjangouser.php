<?php

function GetDBSession()
{
  $dbSession = pg_connect("host=localhost dbname=brouwersapps user=bbt password=1234");
  if (!$dbSession)
  {
    throw new Exception("cannot connect to DBMS: " . pg_last_error());
  }

  return $dbSession;
}


function GetDjangoUser()
{
    $djangoSessionID = $_COOKIE['sessionid'];

    $dbSession = GetDBSession();
    $query =
      "SELECT up.forum_nickname as username, auth_user.email as email ".
      "  FROM auth_user, sessionprofile_sessionprofile sp, general_userprofile up" .
      " WHERE sp.session_id = '" . pg_escape_string($djangoSessionID) . "' " .
      "   AND auth_user.id = sp.user_id
          AND auth_user.id = up.user_id";
    $queryID = pg_query($dbSession, $query);

    if (!$queryID)
    {
      throw new Exception("Could not check whether user was logged in: " , pg_last_error());
    }

    $row = pg_fetch_array($queryID);
    if ($row)
    {
      return $row;
    }

    return null;
}

?>
