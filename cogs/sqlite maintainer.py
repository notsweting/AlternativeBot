import sqlite3

conn = sqlite3.connect('AltBotDataBase.db')
c = conn.cursor()

c.execute('CREATE TABLE MUTEDROLES (ServerID, RoleID)')
c.execute('CREATE TABLE CHANNELLOCK (ChannelID, Overwrites)')
c.execute('CREATE TABLE LOGGING (ServerID, LoggingToggle, LoggingChannelID, \
    OnMsgDeleteToggle, OnBulkMsgDeleteToggle, OnMsgEditToggle, \
    OnReactionClearToggle, OnChannelCreateDeleteToggle, OnChannelEditToggle, \
    OnMemberJoinToggle, OnMemberLeaveToggle, OnMemberEditToggle, \
    OnGuildEditToggle, OnGuildRoleCreateDeleteToggle, OnGuildRoleUpdateToggle, \
    OnGuildMemberBanUnbanToggle, OnGuildMemberKickToggle, OnGuildInviteCreateDeleteToggle)')
c.execute('CREATE TABLE SERVERADMIN (ServerID, Prefix)')