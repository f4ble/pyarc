import time

from sqlalchemy import create_engine, exc, text, func
from sqlalchemy.orm import sessionmaker

from ark.cli import Config
from ark.database.orm_models import Base, WebsiteData, Player, Chat, ChatFilter, Survey, Option, Vote
from ark.database.core import DbCore
from factory import Factory
from ark.cli import *

DbCore = Factory.get('DatabaseCore')

class Db(object):
    """Helper functions for database

    No reason to hate sqlalchemy or spend 30 years learning.
    Write your often-used functions here :)
    """

    @staticmethod
    def keep_alive():
        try:
            resp = DbCore.engine.execute('select 1')
        except exc.SQLAlchemyError as e:
            out('SQL Failure: with keep alive:',e)

    @staticmethod
    def update_last_seen(steam_ids):
        """Update last_seen column on a player

        Args:
            steam_ids: Integer or List of steam id
        Returns:
            True if any updates
        """

        do_commit = False

        if type(steam_ids) == int:
            p = Db.find_player(steam_id=steam_ids)
            if p:
                p.last_seen = text('NOW()')
                DbCore.session.add(p)
                do_commit = True
        else:
            for steam_id in steam_ids:
                p = Db.find_player(steam_id=steam_id)
                if p:
                    p.last_seen = text('NOW()')
                    DbCore.session.add(p)
                    do_commit = True

        if do_commit is True:
            DbCore.commit()
            return True
        return False

    @staticmethod
    def website_data_get(key):
        try:
            return DbCore.session.query(WebsiteData).filter_by(key=key).first()
        except exc.SQLAlchemyError as e:
            out('SQL Failure to get website_data:',e)
            DbCore.reconnect()
            return None


    @staticmethod
    def website_data_set(key,value):
        try:
            data = DbCore.session.query(WebsiteData).filter_by(key=key).first()
        except exc.SQLAlchemyError as e:
            out('SQL Failure - website_data set:',e)
            DbCore.reconnect()
            return False

        if not data:
            data = WebsiteData()

        data.key = key
        data.value = value

        DbCore.session.add(data)
        DbCore.commit()
        return True

    @staticmethod
    def find_player(steam_id=None, steam_name=None, name=None, exact_match=True):
        """Find player by steam_name, name or steam id

        Searches steam_id, steam_name and name. In that order.
        exact_match: If true - On any name search only return if 1 match

        Args:
            steam_name: Default None
            steam_id: Default None
            name: Default None
            exact_match: Bool. Default True.
        Returns:
            Player object or None
        """
        try:
            player = None


            if steam_id:
                player = DbCore.session.query(Player).filter_by(steam_id=steam_id).first()
            elif steam_name:
                players = DbCore.session.query(Player).filter_by(steam_name=steam_name)
                if exact_match:
                    if players.count() == 1:
                        player = players.first()
                else:
                    player = players.first()
            elif name:
                players = DbCore.session.query(Player).filter_by(name=name)
                if exact_match:
                    if players.count() == 1:
                        player = players.first()
                else:
                    player = players.first()
            else:
                out('ERROR: No search parameters in DbCore.find_player')

            if player:
                    return player
            return None
        except exc.SQLAlchemyError as e:
            out('SQL Failure to find player:',e)
            DbCore.reconnect()
            return None


    @staticmethod
    def find_player_wildcard(player_name=None, steam_name=None):
        """Find player by LIKE %name%

        Args:
            player_name: String, default None
            steam_name: String, default None
        Returns:
            Player object or None
        """
        try:
            player = None
            wildcard = '%{}%'.format(player_name)
            if player_name:
                player = DbCore.session.query(Player).filter(Player.name.like(wildcard)).first()
            elif steam_name:
                player = DbCore.session.query(Player).filter(Player.steam_name.like(wildcard)).first()
            else:
                out('ERROR: No search params. DbCore.find_player_wildcard')

            return player
        except exc.SQLAlchemyError as e:
            out('SQL Failure - find player wildcard:',e)
            DbCore.reconnect()
            return None

    @staticmethod
    def create_player(steam_id, steam_name, name=None):
        """Create entry in players table

        Returns:
            Player: Object
            Bool: True if new entry.
        """

        player = Db.find_player(steam_id, steam_name)

        if player is None:
            player = Player(steam_name=steam_name, steam_id=steam_id, name=name, admin=0, last_seen=text("NOW()"), created=text("NOW()"))
            DbCore.session.add(player)
            DbCore.commit()
            return player, True

        return player, False


    @staticmethod
    def update_player(steam_id, steam_name=None, name=None):
        player = Db.find_player(steam_id)
        if player is None:
            return None, False

        altered = False
        if steam_name and player.steam_name != steam_name:
            player.steam_name = steam_name
            altered = True
        if name and player.name != name:
            player.name = name
            altered = True

        if altered:
            DbCore.session.add(player)
            DbCore.commit()
        return True

    @staticmethod
    def create_chat_entry(player_id,name,data):
        entry = Chat(player_id=player_id,name=name,data=data,created=text('NOW()'))
        DbCore.session.add(entry)
        DbCore.commit()
        return entry

    @staticmethod
    def getPlayerCount(active=False):
        try:
            if active is False:
                result = DbCore.session.query(Player)
            else:
                result = DbCore.session.query(Player).filter(func.unix_timestamp(Player.last_seen) >= time.time()-Config.active_player_timeframe)

            return result.count()
        except exc.SQLAlchemyError as e:
            out('SQL Failure - getPlayerCount:',e)
            DbCore.reconnect()
            return None

    @staticmethod
    def check_word(word):
        result = None
        result = DbCore.session.query(ChatFilter).filter_by(word=word).first()
        if result:
            return result
        return None

    @staticmethod
    def add_word(text):
        result=DbCore.session.query(ChatFilter).filter_by(word=text).first()
        if result is None:
            entry = ChatFilter(word=text)
            DbCore.session.add(entry)
            DbCore.session.commit()
            return entry
        else:
            return False

    @staticmethod
    def remove_word(text):
        result=DbCore.session.query(ChatFilter).filter_by(word=text).first()
        if result is not None:
            DbCore.session.query(ChatFilter).filter_by(word=text).delete()
            DbCore.session.commit()
            return text
        else:
            return False

    @staticmethod
    def find_quote(text):
        result=None
        result=DbCore.session.query(Chat).filter_by(id=text).first()
        return result

    @staticmethod
    def add_survey(question):
        result=None
        entry=Survey(question=question,created=text('NOW()'),active="1")
        DbCore.session.add(entry)
        DbCore.session.commit()
        sondage = DbCore.session.query(Sondage).filter_by(question=question).first()
        if sondage is not None:
            return sondage.id
        else:
            return None

    @staticmethod
    def stop_survey(id_survey):
        result=False
        DbCore.session.query(Survey).filter_by(id=id_survey).update({"active":"0"})
        DbCore.session.commit()
        result=DbCore.session.query(Survey).filter_by(id=id_survey).first()
        if result.active is 0:
            return True
        else:
            return False

    @staticmethod
    def start_survey(id_survey):
        result=False
        DbCore.session.query(Survey).filter_by(id=id_survey).update({"active":"1"})
        DbCore.session.commit()
        result=DbCore.session.query(Survey).filter_by(id=id_survey).first()
        if result.active is 1:
            return True
        else:
            return False

    @staticmethod
    def find_survey(id_survey):
        result=None
        if id_survey is None:
            result=DbCore.session.query(Survey).filter_by(active="1").first()
        else:
            result=DbCore.session.query(Survey).filter_by(id=id_survey).first()
        return result

    @staticmethod
    def find_options(id_survey):
        result=None
        options=DbCore.session.query(Option).filter_by(id_survey=id_survey).all()
        for option in options:
            if result is None:
                result=""
            result="{}\n{}-{}".format(result,option.id,option.option)
        return result

    @staticmethod
    def option_exists(id_survey,id_option):
        result=False
        options = None
        options=DbCore.session.query(Option).filter_by(id_survey=id_survey,id=id_option).first()
        if options is not None:
            result=True
        return result

    @staticmethod
    def vote(id_survey,id_option,steam_id,player_name):
        votes = None
        vote=None
        found = False
        id_vote = None
        votes = DbCore.session.query(Vote).filter_by(steam_id=steam_id).all()
        for vote in votes:
            if vote.id_survey is id_survey:
                id_vote = vote.id
        if id_vote is not None:
            DbCore.session.query(Vote).filter_by(id=id_vote).delete()
            DbCore.session.commit()
        entry=Vote(player_name=player_name,steam_id=steam_id,id_survey=id_survey,id_option=id_option)
        DbCore.session.add(entry)
        DbCore.session.commit()
        return True