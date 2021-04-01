import sqlite3

connection = sqlite3.connect('AltBotDataBase.db')
cursor = connection.cursor()

'''
cursor.execute('CREATE TABLE MUTEDROLES(ServerID, RoleID)')
cursor.execute('CREATE TABLE LOGGING(ServerID, LoggingToggle, LoggingChannelID, \
    OnMsgDeleteToggle, OnBulkMsgDeleteToggle, OnMsgEditToggle, OnReactionClearToggle, \
    OnChannelCreateDeleteToggle, OnChannelEditToggle, \
    OnMemberJoinToggle, OnMemberLeaveToggle, OnMemberEditToggle, \
    OnGuildEditToggle, OnGuildRoleCreateDeleteToggle, OnGuildRoleUpdateToggle, \
    OnGuildMemberBanUnbanToggle, OnGuildMemberKickToggle, OnGuildInviteCreateDeleteToggle)')
cursor.execute('CREATE TABLE PREMIUM(UserID, ServerID, PremiumLevel)')
cursor.execute('CREATE TABLE BUGFIX(BugNumber, FixedStatus)')
'''

connection.commit()
connection.close()
