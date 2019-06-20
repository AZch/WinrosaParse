from peewee import *

database = MySQLDatabase('mydb', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'user': 'test', 'password': 'Test_Test123'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Bookmaker(BaseModel):
    base_name = CharField(column_name='BaseName')
    url = CharField(column_name='URL', null=True)
    id_bookmaker = AutoField(column_name='idBookmaker')

    class Meta:
        table_name = 'Bookmaker'

class Resource(BaseModel):
    name = CharField(column_name='Name')
    type_get = CharField(column_name='TypeGet')
    url = CharField(column_name='URL')
    id_resource = AutoField(column_name='idResource')

    class Meta:
        table_name = 'Resource'

class Capper(BaseModel):
    personal_data = CharField(column_name='PersonalData')
    post_data = CharField(column_name='PostData')
    prev_data = CharField(column_name='PrevData')
    resource_id_resource = ForeignKeyField(column_name='Resource_idResource', field='id_resource', model=Resource)
    id_capper = IntegerField(column_name='idCapper')

    class Meta:
        table_name = 'Capper'
        indexes = (
            (('id_capper', 'resource_id_resource'), True),
        )
        primary_key = CompositeKey('id_capper', 'resource_id_resource')

class Forecast(BaseModel):
    base_name = CharField(column_name='BaseName')
    id_forecast = AutoField(column_name='idForecast')

    class Meta:
        table_name = 'Forecast'

class Ligue(BaseModel):
    base_name = CharField(column_name='BaseName')
    code = CharField(column_name='Code', null=True)
    id_ligue = AutoField(column_name='idLigue')

    class Meta:
        table_name = 'Ligue'

class Sport(BaseModel):
    base_name = CharField(column_name='BaseName')
    code = CharField(column_name='Code', null=True)
    id_sport = AutoField(column_name='idSport')

    class Meta:
        table_name = 'Sport'

class Bet(BaseModel):
    bookmaker_id_bookmaker = ForeignKeyField(column_name='Bookmaker_idBookmaker', field='id_bookmaker', model=Bookmaker)
    capper_resource_id_resource = ForeignKeyField(column_name='Capper_Resource_idResource', field='resource_id_resource', model=Capper)
    capper_id_capper = ForeignKeyField(backref='Capper_capper_id_capper_set', column_name='Capper_idCapper', field='id_capper', model=Capper)
    forecast_id_forecast = ForeignKeyField(column_name='Forecast_idForecast', field='id_forecast', model=Forecast)
    kf = CharField(column_name='KF')
    ligue_id_ligue = ForeignKeyField(column_name='Ligue_idLigue', field='id_ligue', model=Ligue)
    percent = CharField(column_name='Percent')
    result = CharField(column_name='Result', constraints=[SQL("DEFAULT '0.0'")])
    sport_id_sport = ForeignKeyField(column_name='Sport_idSport', field='id_sport', model=Sport)
    time_event = DateTimeField(column_name='TimeEvent')
    time_input = DateTimeField(column_name='TimeInput')
    val_forecast = CharField(column_name='ValForecast')
    id_bet = IntegerField(column_name='idBet')

    class Meta:
        table_name = 'Bet'
        indexes = (
            (('capper_id_capper', 'capper_resource_id_resource'), False),
            (('id_bet', 'forecast_id_forecast', 'sport_id_sport', 'ligue_id_ligue', 'capper_id_capper', 'capper_resource_id_resource', 'bookmaker_id_bookmaker'), True),
        )
        primary_key = CompositeKey('bookmaker_id_bookmaker', 'capper_id_capper', 'capper_resource_id_resource', 'forecast_id_forecast', 'id_bet', 'ligue_id_ligue', 'sport_id_sport')

class BookMakerNames(BaseModel):
    bookmaker_id_bookmaker = ForeignKeyField(column_name='Bookmaker_idBookmaker', field='id_bookmaker', model=Bookmaker)
    other_name = CharField(column_name='OtherName')
    id_book_maker_names = IntegerField(column_name='idBookMakerNames')

    class Meta:
        table_name = 'BookMakerNames'
        indexes = (
            (('id_book_maker_names', 'bookmaker_id_bookmaker'), True),
        )
        primary_key = CompositeKey('bookmaker_id_bookmaker', 'id_book_maker_names')

class User(BaseModel):
    login_user = CharField(column_name='LoginUser')
    password_user = CharField(column_name='PasswordUser')
    id_user = AutoField(column_name='idUser')

    class Meta:
        table_name = 'User'

class CapperUser(BaseModel):
    capper_resource_id_resource = ForeignKeyField(column_name='Capper_Resource_idResource', field='resource_id_resource', model=Capper)
    capper_id_capper = ForeignKeyField(backref='Capper_capper_id_capper_set', column_name='Capper_idCapper', field='id_capper', model=Capper)
    user_id_user = ForeignKeyField(column_name='User_idUser', field='id_user', model=User)
    id_capper_user = AutoField(column_name='idCapperUser')

    class Meta:
        table_name = 'CapperUser'
        indexes = (
            (('capper_id_capper', 'capper_resource_id_resource'), False),
        )

class Descs(BaseModel):
    desc_code = CharField(column_name='DescCode')
    desc_data = CharField(column_name='DescData')
    id_descs_bet = AutoField(column_name='idDescsBet')

    class Meta:
        table_name = 'Descs'

class DescBet(BaseModel):
    bet_resource_resource_id_resource = IntegerField(column_name='Bet_Resource_Resource_idResource')
    bet_resource_id_capper = IntegerField(column_name='Bet_Resource_idCapper')
    bet_id_bet = ForeignKeyField(column_name='Bet_idBet', field='id_bet', model=Bet)
    descs_id_descs_bet = ForeignKeyField(column_name='Descs_idDescsBet', field='id_descs_bet', model=Descs)
    id_desc_bet = AutoField(column_name='idDescBet')

    class Meta:
        table_name = 'DescBet'
        indexes = (
            (('bet_id_bet', 'bet_resource_id_capper', 'bet_resource_resource_id_resource'), False),
        )

class Filter(BaseModel):
    ligue_sport_id_sport = IntegerField(column_name='Ligue_Sport_idSport')
    ligue_id_ligue = IntegerField(column_name='Ligue_idLigue')
    type_filter = IntegerField(column_name='TypeFilter')
    id_filter = IntegerField(column_name='idFilter')

    class Meta:
        table_name = 'Filter'
        indexes = (
            (('id_filter', 'ligue_id_ligue', 'ligue_sport_id_sport'), True),
        )
        primary_key = CompositeKey('id_filter', 'ligue_id_ligue', 'ligue_sport_id_sport')

class UserFilter(BaseModel):
    filter_ligue_sport_id_sport = ForeignKeyField(column_name='Filter_Ligue_Sport_idSport', field='ligue_sport_id_sport', model=Filter)
    filter_ligue_id_ligue = ForeignKeyField(backref='Filter_filter_ligue_id_ligue_set', column_name='Filter_Ligue_idLigue', field='ligue_id_ligue', model=Filter)
    filter_id_filter = ForeignKeyField(backref='Filter_filter_id_filter_set', column_name='Filter_idFilter', field='id_filter', model=Filter)
    user_id_user = ForeignKeyField(column_name='User_idUser', field='id_user', model=User)
    id_user_filter = AutoField(column_name='idUserFilter')
    is_public = IntegerField(column_name='isPublic')

    class Meta:
        table_name = 'UserFilter'
        indexes = (
            (('filter_id_filter', 'filter_ligue_id_ligue', 'filter_ligue_sport_id_sport'), False),
        )

class FilterCapper(BaseModel):
    capper_resource_id_resource = ForeignKeyField(column_name='Capper_Resource_idResource', field='resource_id_resource', model=Capper)
    capper_id_capper = ForeignKeyField(backref='Capper_capper_id_capper_set', column_name='Capper_idCapper', field='id_capper', model=Capper)
    price_bet = FloatField(column_name='PriceBet')
    user_filter_id_user_filter = ForeignKeyField(column_name='UserFilter_idUserFilter', field='id_user_filter', model=UserFilter)
    id_filter_capper = AutoField(column_name='idFilterCapper')

    class Meta:
        table_name = 'FilterCapper'
        indexes = (
            (('capper_id_capper', 'capper_resource_id_resource'), False),
        )

class FilterForecast(BaseModel):
    filter_ligue_sport_id_sport = ForeignKeyField(column_name='Filter_Ligue_Sport_idSport', field='ligue_sport_id_sport', model=Filter)
    filter_ligue_id_ligue = ForeignKeyField(backref='Filter_filter_ligue_id_ligue_set', column_name='Filter_Ligue_idLigue', field='ligue_id_ligue', model=Filter)
    filter_id_filter = ForeignKeyField(backref='Filter_filter_id_filter_set', column_name='Filter_idFilter', field='id_filter', model=Filter)
    forecast_id_forecast = ForeignKeyField(column_name='Forecast_idForecast', field='id_forecast', model=Forecast)
    id_filter_forecast = AutoField(column_name='idFilterForecast')

    class Meta:
        table_name = 'FilterForecast'
        indexes = (
            (('filter_id_filter', 'filter_ligue_id_ligue', 'filter_ligue_sport_id_sport'), False),
        )

class FilterLigue(BaseModel):
    filter_ligue_sport_id_sport = ForeignKeyField(column_name='Filter_Ligue_Sport_idSport', field='ligue_sport_id_sport', model=Filter)
    filter_ligue_id_ligue = ForeignKeyField(backref='Filter_filter_ligue_id_ligue_set', column_name='Filter_Ligue_idLigue', field='ligue_id_ligue', model=Filter)
    filter_id_filter = ForeignKeyField(backref='Filter_filter_id_filter_set', column_name='Filter_idFilter', field='id_filter', model=Filter)
    ligue_sport_id_sport = IntegerField(column_name='Ligue_Sport_idSport')
    ligue_id_ligue = ForeignKeyField(column_name='Ligue_idLigue', field='id_ligue', model=Ligue)
    id_filter_ligue = AutoField(column_name='idFilterLigue')

    class Meta:
        table_name = 'FilterLigue'
        indexes = (
            (('filter_id_filter', 'filter_ligue_id_ligue', 'filter_ligue_sport_id_sport'), False),
            (('ligue_id_ligue', 'ligue_sport_id_sport'), False),
        )

class FilterSport(BaseModel):
    filter_ligue_sport_id_sport = ForeignKeyField(column_name='Filter_Ligue_Sport_idSport', field='ligue_sport_id_sport', model=Filter)
    filter_ligue_id_ligue = ForeignKeyField(backref='Filter_filter_ligue_id_ligue_set', column_name='Filter_Ligue_idLigue', field='ligue_id_ligue', model=Filter)
    filter_id_filter = ForeignKeyField(backref='Filter_filter_id_filter_set', column_name='Filter_idFilter', field='id_filter', model=Filter)
    sport_id_sport = ForeignKeyField(column_name='Sport_idSport', field='id_sport', model=Sport)
    id_filter_sport = AutoField(column_name='idFilterSport')

    class Meta:
        table_name = 'FilterSport'
        indexes = (
            (('filter_id_filter', 'filter_ligue_id_ligue', 'filter_ligue_sport_id_sport'), False),
        )

class ForecastNames(BaseModel):
    forecast_id_forecast = ForeignKeyField(column_name='Forecast_idForecast', field='id_forecast', model=Forecast)
    other_name = CharField(column_name='OtherName')
    id_forecast_names = IntegerField(column_name='idForecastNames')

    class Meta:
        table_name = 'ForecastNames'
        indexes = (
            (('id_forecast_names', 'forecast_id_forecast'), True),
        )
        primary_key = CompositeKey('forecast_id_forecast', 'id_forecast_names')

class LigueNames(BaseModel):
    ligue_sport_id_sport = IntegerField(column_name='Ligue_Sport_idSport')
    ligue_id_ligue = ForeignKeyField(column_name='Ligue_idLigue', field='id_ligue', model=Ligue)
    other_name = CharField(column_name='OtherName')
    id_ligue_names = IntegerField(column_name='idLigueNames')

    class Meta:
        table_name = 'LigueNames'
        indexes = (
            (('id_ligue_names', 'ligue_id_ligue', 'ligue_sport_id_sport'), True),
            (('ligue_id_ligue', 'ligue_sport_id_sport'), False),
        )
        primary_key = CompositeKey('id_ligue_names', 'ligue_id_ligue', 'ligue_sport_id_sport')

class ResourceCommand(BaseModel):
    data = CharField(column_name='Data')
    desc = CharField(column_name='Desc')
    resource_id_resource = ForeignKeyField(column_name='Resource_idResource', field='id_resource', model=Resource)
    id_resource_command = IntegerField(column_name='idResourceCommand')

    class Meta:
        table_name = 'ResourceCommand'
        indexes = (
            (('id_resource_command', 'resource_id_resource'), True),
        )
        primary_key = CompositeKey('id_resource_command', 'resource_id_resource')

class SportNames(BaseModel):
    other_name = CharField(column_name='OtherName')
    sport_id_sport = ForeignKeyField(column_name='Sport_idSport', field='id_sport', model=Sport)
    id_sport_names = IntegerField(column_name='idSportNames')

    class Meta:
        table_name = 'SportNames'
        indexes = (
            (('id_sport_names', 'sport_id_sport'), True),
        )
        primary_key = CompositeKey('id_sport_names', 'sport_id_sport')

class Team(BaseModel):
    base_name = CharField(column_name='BaseName')
    id_team = AutoField(column_name='idTeam')

    class Meta:
        table_name = 'Team'

class TeamBet(BaseModel):
    bet_id_bet = ForeignKeyField(column_name='Bet_idBet', field='id_bet', model=Bet)
    team_id_team = ForeignKeyField(column_name='Team_idTeam', field='id_team', model=Team)
    id_team_bet = AutoField(column_name='idTeamBet')

    class Meta:
        table_name = 'TeamBet'

class TeamNames(BaseModel):
    other_name = CharField(column_name='OtherName')
    team_id_team = ForeignKeyField(column_name='Team_idTeam', field='id_team', model=Team)
    id_team_names = IntegerField(column_name='idTeamNames')

    class Meta:
        table_name = 'TeamNames'
        indexes = (
            (('id_team_names', 'team_id_team'), True),
        )
        primary_key = CompositeKey('id_team_names', 'team_id_team')

class UserBk(BaseModel):
    bookmaker_id_bookmaker = ForeignKeyField(column_name='Bookmaker_idBookmaker', field='id_bookmaker', model=Bookmaker)
    login_bk = CharField(column_name='LoginBK')
    user_b_kcol = CharField(column_name='UserBKcol')
    user_id_user = ForeignKeyField(column_name='User_idUser', field='id_user', model=User)
    id_user_bk = IntegerField(column_name='idUserBK')

    class Meta:
        table_name = 'UserBK'
        indexes = (
            (('id_user_bk', 'user_id_user'), True),
        )
        primary_key = CompositeKey('id_user_bk', 'user_id_user')

class UserBet(BaseModel):
    bet_forecast_id_forecast = ForeignKeyField(column_name='Bet_Forecast_idForecast', field='forecast_id_forecast', model=Bet)
    bet_ligue_sport_id_sport = IntegerField(column_name='Bet_Ligue_Sport_idSport')
    bet_ligue_id_ligue = IntegerField(column_name='Bet_Ligue_idLigue')
    bet_resource_resource_id_resource = IntegerField(column_name='Bet_Resource_Resource_idResource')
    bet_resource_id_capper = IntegerField(column_name='Bet_Resource_idCapper')
    bet_id_bet = ForeignKeyField(backref='Bet_bet_id_bet_set', column_name='Bet_idBet', field='id_bet', model=Bet)
    filter_capper_id_filter_capper = ForeignKeyField(column_name='FilterCapper_idFilterCapper', field='id_filter_capper', model=FilterCapper)
    real_kf = FloatField(column_name='RealKF')
    real_price_bet = FloatField(column_name='RealPriceBet')
    real_result_bet = FloatField(column_name='RealResultBet')
    id_user_bet = AutoField(column_name='idUserBet')

    class Meta:
        table_name = 'UserBet'
        indexes = (
            (('bet_id_bet', 'bet_forecast_id_forecast'), False),
            (('bet_id_bet', 'bet_resource_id_capper', 'bet_resource_resource_id_resource', 'bet_ligue_id_ligue', 'bet_ligue_sport_id_sport', 'bet_forecast_id_forecast'), False),
        )

