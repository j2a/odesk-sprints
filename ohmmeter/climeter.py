#!/usr/bin/env python

import odesk
import datetime


class Time(object):
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

    def __str__(self):
        return '%01d:%02d' % (self.hours, self.minutes)

    def __repr__(self):
        return '<Time: %s>' % self.__str__()

    @classmethod
    def from_hours(cls, value):
        value = float(value)
        hours = int(value)
        minutes = int( (value - hours) * 60 )
        return cls(hours, minutes)

    @classmethod
    def from_minutes(cls, value):
        value = int(value)
        hours, minutes = divmod(value, 60)
        return cls(hours, minutes)

    @classmethod
    def from_seconds(cls, value):
        value = int(value)
        minutes = round(value / 60.0)
        return cls.from_minutes(minutes)


    def __add__(self, other):
        if isinstance(other, int) and other == 0:
            return self
        elif isinstance(other, float) and other == 0.0:
            return self
        elif not isinstance(other, Time):
            raise TypeError(
                "Unsupport adding Time and %s" % type(other).__name__)
        hours = self.hours + other.hours
        minutes = self.minutes + other.minutes
        if minutes > 60:
            additional_hours, left_minutes = divmod(minutes, 60)
            hours += additional_hours
            minutes = left_minutes
        return Time(hours, minutes)

    def __radd__(self, other):
        return self.__add__(other)


def meter(*creds):
    client = odesk.Client(*creds)
    print "By report: %s" % by_report(client)
    print "By diary: %s" % by_workdiary(client)


def by_report(client):
    user = client.auth.check_token()[1]['uid']
    cols = ['worked_on', 'team_id', 'hours']
    query = odesk.Query(
        select=cols,
        where=odesk.Q('worked_on') == datetime.date.today())
    report = client.time_reports.get_provider_report(user, query)
    meter = {}
    for row in report['table']['rows']:
        data = dict(zip(cols, [c['v'] for c in row['c']]))
        key = data['team_id']
        meter[key] = Time.from_hours(meter.get(key, 0)) + \
            Time.from_hours(float(data['hours']))
    overall = sum(meter.values())
    meter['overall'] = overall
    return meter


def by_workdiary(client):
    user = client.auth.check_token()[1]['uid']
    teams = [t['id'] for t in client.team.get_teamrooms()]
    meter = {}
    for team in teams:
        header, workdiaries = client.team.get_workdiaries(team, user)
        # oDesk UI have the same method of counting activity:
        # count of active cells * 10minutes
        meter[team] = Time.from_minutes(len(workdiaries) * 10)
    overall = sum(meter.values())
    meter['overall'] = overall
    return meter


if __name__ == '__main__':
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(['creds.ini'])
    meter(
        cfg.get('odesk-auth', 'public-key'),
        cfg.get('odesk-auth', 'secret-key'),
        cfg.get('odesk-auth', 'token'))
