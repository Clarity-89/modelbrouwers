<?php


function GetDBSession()
{
  global $django_dbname, $django_dbuser, $django_dbpasswd;
  $dbSession = pg_connect("dbname={$django_dbname} user=${django_dbuser} password={$django_dbpasswd}");
  if (!$dbSession)
  {
    throw new Exception("cannot connect to DBMS: " . pg_last_error());
  }

  return $dbSession;
}


function GetDjangoUser()
{
    $djangoSessionID = $_COOKIE['mbsessionid'];
    if(!$djangoSessionID){
      $djangoSessionID = $_COOKIE['sessionid'];
    }

    $dbSession = GetDBSession();
    $query =
      "SELECT up.forum_nickname as username, users_user.email as email ".
      "  FROM users_user, sessionprofile_sessionprofile sp, general_userprofile up" .
      " WHERE sp.session_id = '" . pg_escape_string($djangoSessionID) . "' " .
      "   AND users_user.id = sp.user_id
          AND users_user.id = up.user_id";
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

    pg_close($dbSession);

    return null;
}

?>
