from __future__ import absolute_import, division, print_function, unicode_literals
import openreview
import pytest
import requests
import datetime
import time
import os
import re
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

class TestDoubleBlindConference():

    def test_create_conference(self, client):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.has_area_chairs(True)
        conference = builder.get_result()
        assert conference, 'conference is None'

        groups = conference.get_conference_groups()
        assert groups
        assert groups[0].id == 'AKBC.ws'
        assert groups[0].readers == ['everyone']
        assert groups[0].nonreaders == []
        assert groups[0].writers == ['AKBC.ws']
        assert groups[0].signatures == ['~Super_User1']
        assert groups[0].signatories == ['AKBC.ws']
        assert groups[0].members == []
        assert groups[1].id == 'AKBC.ws/2019'
        assert groups[1].readers == ['everyone']
        assert groups[1].nonreaders == []
        assert groups[1].writers == ['AKBC.ws/2019']
        assert groups[1].signatures == ['~Super_User1']
        assert groups[1].signatories == ['AKBC.ws/2019']
        assert groups[1].members == []
        assert groups[2].id == 'AKBC.ws/2019/Conference'
        assert groups[2].readers == ['everyone']
        assert groups[2].nonreaders == []
        assert groups[2].writers == ['AKBC.ws/2019/Conference']
        assert groups[2].signatures == ['AKBC.ws/2019/Conference']
        assert groups[2].signatories == ['AKBC.ws/2019/Conference']
        assert groups[2].members == ['AKBC.ws/2019/Conference/Program_Chairs']
        assert '"title": "AKBC.ws/2019/Conference"' in groups[2].web

        assert client.get_group(id = 'AKBC.ws')
        assert client.get_group(id = 'AKBC.ws/2019')
        assert client.get_group(id = 'AKBC.ws/2019/Conference')

        resp = requests.get('http://localhost:3030/group?id=AKBC.ws')
        assert resp.status_code == 200

        resp = requests.get('http://localhost:3030/group?id=AKBC.ws/2019')
        assert resp.status_code == 200

        resp = requests.get('http://localhost:3030/group?id=AKBC.ws/2019/Conference')
        assert resp.status_code == 200

    def test_create_conference_with_name(self, client):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_conference_name('Automated Knowledge Base Construction')
        builder.has_area_chairs(True)

        conference = builder.get_result()
        assert conference, 'conference is None'

        groups = conference.get_conference_groups()
        assert groups
        assert groups[0].id == 'AKBC.ws'
        assert groups[0].readers == ['everyone']
        assert groups[0].nonreaders == []
        assert groups[0].writers == ['AKBC.ws']
        assert groups[0].signatures == ['~Super_User1']
        assert groups[0].signatories == ['AKBC.ws']
        assert groups[0].members == []
        assert groups[1].id == 'AKBC.ws/2019'
        assert groups[1].readers == ['everyone']
        assert groups[1].nonreaders == []
        assert groups[1].writers == ['AKBC.ws/2019']
        assert groups[1].signatures == ['~Super_User1']
        assert groups[1].signatories == ['AKBC.ws/2019']
        assert groups[1].members == []
        assert groups[2].id == 'AKBC.ws/2019/Conference'
        assert groups[2].readers == ['everyone']
        assert groups[2].nonreaders == []
        assert groups[2].writers == ['AKBC.ws/2019/Conference']
        assert groups[2].signatures == ['AKBC.ws/2019/Conference']
        assert groups[2].signatories == ['AKBC.ws/2019/Conference']
        assert groups[2].members == ['AKBC.ws/2019/Conference/Program_Chairs']
        assert '"title": "AKBC.ws/2019/Conference"' in groups[2].web
        assert '"subtitle": "Automated Knowledge Base Construction"' in groups[2].web

        assert client.get_group(id = 'AKBC.ws')
        assert client.get_group(id = 'AKBC.ws/2019')
        assert client.get_group(id = 'AKBC.ws/2019/Conference')

        resp = requests.get('http://localhost:3030/group?id=AKBC.ws')
        assert resp.status_code == 200

        resp = requests.get('http://localhost:3030/group?id=AKBC.ws/2019')
        assert resp.status_code == 200

        resp = requests.get('http://localhost:3030/group?id=AKBC.ws/2019/Conference')
        assert resp.status_code == 200

    def test_create_conference_with_headers(self, client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_conference_name('Automated Knowledge Base Construction')
        builder.set_homepage_header({
            'title': 'AKBC 2019',
            'subtitle': 'Automated Knowledge Base Construction',
            'location': 'Amherst, Massachusetts, United States',
            'date': 'May 20 - May 21, 2019',
            'website': 'http://www.akbc.ws/2019/',
            'instructions': '<p><strong>Important Information</strong>\
                <ul>\
                <li>Note to Authors, Reviewers and Area Chairs: Please update your OpenReview profile to have all your recent emails.</li>\
                <li>AKBC 2019 Conference submissions are now open.</li>\
                <li>For more details refer to the <a href="http://www.akbc.ws/2019/cfp/">AKBC 2019 - Call for Papers</a>.</li>\
                </ul></p> \
                <p><strong>Questions or Concerns</strong></p>\
                <p><ul>\
                <li>Please contact the AKBC 2019 Program Chairs at \
                <a href="mailto:info@akbc.ws">info@akbc.ws</a> with any questions or concerns about conference administration or policy.</li>\
                <li>Please contact the OpenReview support team at \
                <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform.</li>\
                </ul></p>',
            'deadline': 'Submission Deadline: Midnight Pacific Time, Friday, November 16, 2018'
        })
        builder.has_area_chairs(True)

        conference = builder.get_result()
        assert conference, 'conference is None'

        groups = conference.get_conference_groups()
        assert groups
        assert groups[0].id == 'AKBC.ws'
        assert groups[0].readers == ['everyone']
        assert groups[0].nonreaders == []
        assert groups[0].writers == ['AKBC.ws']
        assert groups[0].signatures == ['~Super_User1']
        assert groups[0].signatories == ['AKBC.ws']
        assert groups[0].members == []
        assert groups[1].id == 'AKBC.ws/2019'
        assert groups[1].readers == ['everyone']
        assert groups[1].nonreaders == []
        assert groups[1].writers == ['AKBC.ws/2019']
        assert groups[1].signatures == ['~Super_User1']
        assert groups[1].signatories == ['AKBC.ws/2019']
        assert groups[1].members == []
        assert groups[2].id == 'AKBC.ws/2019/Conference'
        assert groups[2].readers == ['everyone']
        assert groups[2].nonreaders == []
        assert groups[2].writers == ['AKBC.ws/2019/Conference']
        assert groups[2].signatures == ['AKBC.ws/2019/Conference']
        assert groups[2].signatories == ['AKBC.ws/2019/Conference']
        assert groups[2].members == ['AKBC.ws/2019/Conference/Program_Chairs']
        assert '"title": "AKBC 2019"' in groups[2].web
        assert '"subtitle": "Automated Knowledge Base Construction"' in groups[2].web
        assert '"location": "Amherst, Massachusetts, United States"' in groups[2].web
        assert '"date": "May 20 - May 21, 2019"' in groups[2].web
        assert '"website": "http://www.akbc.ws/2019/"' in groups[2].web
        assert 'Important Information' in groups[2].web
        assert '"deadline": "Submission Deadline: Midnight Pacific Time, Friday, November 16, 2018"' in groups[2].web
        #assert "var BLIND_SUBMISSION_ID = 'AKBC.ws/2019/Conference/-/Blind_Submission';" in groups[2].web

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference")
        assert "AKBC 2019 Conference | OpenReview" in selenium.title
        header = selenium.find_element_by_id('header')
        assert header
        assert "AKBC 2019" == header.find_element_by_tag_name("h1").text
        assert "Automated Knowledge Base Construction" == header.find_element_by_tag_name("h3").text
        assert "Amherst, Massachusetts, United States" == header.find_element_by_xpath(".//span[@class='venue-location']").text
        assert "May 20 - May 21, 2019" == header.find_element_by_xpath(".//span[@class='venue-date']").text
        assert "http://www.akbc.ws/2019/" == header.find_element_by_xpath(".//span[@class='venue-website']/a").text
        invitation_panel = selenium.find_element_by_id('invitation')
        assert invitation_panel
        assert len(invitation_panel.find_elements_by_tag_name('div')) == 0
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        with pytest.raises(NoSuchElementException):
            notes_panel.find_element_by_class_name('spinner-container')

    def test_enable_submissions(self, client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_conference_name('Automated Knowledge Base Construction')
        builder.set_homepage_header({
            'title': 'AKBC 2019',
            'subtitle': 'Automated Knowledge Base Construction',
            'location': 'Amherst, Massachusetts, United States',
            'date': 'May 20 - May 21, 2019',
            'website': 'http://www.akbc.ws/2019/',
            'instructions': '<p><strong>Important Information</strong>\
                <ul>\
                <li>Note to Authors, Reviewers and Area Chairs: Please update your OpenReview profile to have all your recent emails.</li>\
                <li>AKBC 2019 Conference submissions are now open.</li>\
                <li>For more details refer to the <a href="http://www.akbc.ws/2019/cfp/">AKBC 2019 - Call for Papers</a>.</li>\
                </ul></p> \
                <p><strong>Questions or Concerns</strong></p>\
                <p><ul>\
                <li>Please contact the AKBC 2019 Program Chairs at \
                <a href="mailto:info@akbc.ws">info@akbc.ws</a> with any questions or concerns about conference administration or policy.</li>\
                <li>Please contact the OpenReview support team at \
                <a href="mailto:info@openreview.net">info@openreview.net</a> with any questions or concerns about the OpenReview platform.</li>\
                </ul></p>',
            'deadline': 'Submission Deadline: Midnight Pacific Time, Friday, November 16, 2018'
        })
        now = datetime.datetime.utcnow()
        builder.has_area_chairs(True)
        builder.set_submission_stage(double_blind = True, public = True, due_date = now + datetime.timedelta(minutes = 10))
        conference = builder.get_result()

        invitation = client.get_invitation(conference.get_submission_id())
        assert invitation
        assert invitation.duedate == openreview.tools.datetime_millis(now + datetime.timedelta(minutes = 10))
        assert invitation.expdate == openreview.tools.datetime_millis(now + datetime.timedelta(minutes = 40))

        posted_invitation = client.get_invitation(id = 'AKBC.ws/2019/Conference/-/Submission')
        assert posted_invitation
        assert posted_invitation.duedate == openreview.tools.datetime_millis(now + datetime.timedelta(minutes = 10))
        assert posted_invitation.expdate == openreview.tools.datetime_millis(now + datetime.timedelta(minutes = 40))

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference")

        assert "AKBC 2019 Conference | OpenReview" in selenium.title
        header = selenium.find_element_by_id('header')
        assert header
        assert "AKBC 2019" == header.find_element_by_tag_name("h1").text
        assert "Automated Knowledge Base Construction" == header.find_element_by_tag_name("h3").text
        assert "Amherst, Massachusetts, United States" == header.find_element_by_xpath(".//span[@class='venue-location']").text
        assert "May 20 - May 21, 2019" == header.find_element_by_xpath(".//span[@class='venue-date']").text
        assert "http://www.akbc.ws/2019/" == header.find_element_by_xpath(".//span[@class='venue-website']/a").text
        invitation_panel = selenium.find_element_by_id('invitation')
        assert invitation_panel
        assert len(invitation_panel.find_elements_by_tag_name('div')) == 1
        assert 'AKBC 2019 Conference Submission' == invitation_panel.find_element_by_class_name('btn').text
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('your-consoles')
        assert len(tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')) == 0
        assert tabs.find_element_by_id('recent-activity')
        assert len(tabs.find_element_by_id('recent-activity').find_elements_by_tag_name('ul')) == 0

    def test_post_submissions(self, client, test_client, peter_client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_conference_short_name('AKBC 2019')
        builder.set_authorpage_header({
            'title': 'Author Console',
            'instructions': 'Instructions for author console',
            'schedule': 'This is the author schedule'
        })
        now = datetime.datetime.utcnow()
        builder.has_area_chairs(True)
        builder.set_submission_stage(double_blind = True, public = True, due_date = now + datetime.timedelta(minutes = 10), subject_areas = ['Machine Learning',
            'Natural Language Processing',
            'Information Extraction',
            'Question Answering',
            'Reasoning',
            'Databases',
            'Information Integration',
            'Knowledge Representation',
            'Semantic Web',
            'Search',
            'Applications: Science',
            'Applications: Biomedicine',
            'Applications: Other',
            'Relational AI',
            'Fairness',
            'Human computation',
            'Crowd-sourcing',
            'Other'], additional_fields = {
                'archival_status': {
                    'description': 'Authors can change the archival/non-archival status up until the decision deadline',
                    'value-radio': [
                        'Archival',
                        'Non-Archival'
                    ],
                    'required': True
                }
            })

        conference = builder.get_result()

        invitation = client.get_invitation(conference.get_submission_id())
        assert invitation
        assert 'subject_areas' in invitation.reply['content']
        assert 'Question Answering' in invitation.reply['content']['subject_areas']['values-dropdown']
        assert 'archival_status' in invitation.reply['content']
        assert 10 == invitation.reply['content']['archival_status']['order']

        note = openreview.Note(invitation = invitation.id,
            readers = [conference.id, '~Test_User1', 'peter@mail.com', 'andrew@mail.com'],
            writers = [conference.id, '~Test_User1', 'peter@mail.com', 'andrew@mail.com'],
            signatures = ['~Test_User1'],
            content = {
                'title': 'Paper title',
                'abstract': 'This is an abstract',
                'authorids': ['test@mail.com', 'peter@mail.com', 'andrew@mail.com'],
                'authors': ['Test User', 'Peter User', 'Andrew Mc'],
                'archival_status': 'Archival',
                'subject_areas': [
                    'Databases',
                    'Information Integration',
                    'Knowledge Representation',
                    'Semantic Web'
                ]
            }
        )
        url = test_client.put_attachment(os.path.join(os.path.dirname(__file__), 'data/paper.pdf'), conference.get_submission_id(), 'pdf')
        note.content['pdf'] = url
        test_client.post_note(note)

        # Author user
        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference", test_client.token)
        invitation_panel = selenium.find_element_by_id('invitation')
        assert invitation_panel
        assert len(invitation_panel.find_elements_by_tag_name('div')) == 1
        assert 'AKBC 2019 Conference Submission' == invitation_panel.find_element_by_class_name('btn').text
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('your-consoles')
        assert len(tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')) == 1
        console = tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')[0]
        assert 'Author Console' == console.find_element_by_tag_name('a').text
        assert tabs.find_element_by_id('recent-activity')
        assert len(tabs.find_element_by_id('recent-activity').find_elements_by_class_name('activity-list')) == 1

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference/Authors", test_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('author-tasks')
        assert tabs.find_element_by_id('your-submissions')
        papers = tabs.find_element_by_id('your-submissions').find_element_by_class_name('console-table')
        assert len(papers.find_elements_by_tag_name('tr')) == 2

        # Guest user
        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference")
        invitation_panel = selenium.find_element_by_id('invitation')
        assert invitation_panel
        assert len(invitation_panel.find_elements_by_tag_name('div')) == 1
        assert 'AKBC 2019 Conference Submission' == invitation_panel.find_element_by_class_name('btn').text
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('your-consoles')
        assert len(tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')) == 0
        assert tabs.find_element_by_id('recent-activity')
        assert len(tabs.find_element_by_id('recent-activity').find_elements_by_class_name('activity-list')) == 0

        # Co-author user
        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference", peter_client.token)
        invitation_panel = selenium.find_element_by_id('invitation')
        assert invitation_panel
        assert len(invitation_panel.find_elements_by_tag_name('div')) == 1
        assert 'AKBC 2019 Conference Submission' == invitation_panel.find_element_by_class_name('btn').text
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('your-consoles')
        assert len(tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')) == 1
        console = tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')[0]
        assert 'Author Console' == console.find_element_by_tag_name('a').text
        assert tabs.find_element_by_id('recent-activity')
        assert len(tabs.find_element_by_id('recent-activity').find_elements_by_class_name('activity-list')) == 1

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference/Authors", peter_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('author-tasks')
        assert tabs.find_element_by_id('your-submissions')
        papers = tabs.find_element_by_id('your-submissions').find_element_by_class_name('console-table')
        assert len(papers.find_elements_by_tag_name('tr')) == 2

    def test_recruit_reviewers(self, client, selenium, request_page, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_conference_short_name('AKBC 2019')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        conference = builder.get_result()

        pc_client = helpers.create_user(email = 'akbc_pc_1@akbc.ws', first = 'AKBC', last = 'PCOne')
        conference.set_program_chairs(emails = ['akbc_pc_1@akbc.ws'])

        result = conference.recruit_reviewers(['mbok@mail.com', 'Mohit@mail.com'])
        assert result
        assert len(result['invited']) == 2
        assert len(result['reminded']) == 0
        assert not result['already_invited']
        assert 'mbok@mail.com' in result['invited']
        assert 'mohit@mail.com' in result['invited']

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert group.id == 'AKBC.ws/2019/Conference/Reviewers'
        assert 'AKBC.ws/2019/Conference/Area_Chairs' in group.readers
        assert len(group.members) == 0

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Invited')
        assert group
        assert len(group.members) == 2

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        result = conference.recruit_reviewers(invitees = ['michael@mail.com'], invitee_names = ['Michael Spector'])
        assert result
        assert len(result['invited']) == 1
        assert len(result['reminded']) == 0
        assert not result['already_invited']
        assert 'michael@mail.com' in result['invited']

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 0

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Invited')
        assert group
        assert len(group.members) == 3

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        invitation = client.get_invitation('AKBC.ws/2019/Conference/-/Recruit_Reviewers')
        assert invitation
        assert invitation.process
        assert invitation.web

        messages = client.get_messages(to = 'michael@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        text = messages[0]['content']['text']
        assert 'Dear Michael Spector,' in text
        assert 'You have been nominated by the program chair committee of AKBC 2019' in text

        messages = client.get_messages(to = 'mbok@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        assert messages
        assert len(messages) == 1

        # Test if the reminder mail has "Dear invitee" for unregistered users in case the name is not provided to recruit_reviewers
        result = conference.recruit_reviewers(remind = True, invitees = ['mbok@mail.com'])
        assert result
        assert len(result['invited']) == 0
        assert len(result['reminded']) == 3
        assert 'mbok@mail.com' in result['reminded']
        assert 'mohit@mail.com' in result['reminded']
        assert 'michael@mail.com' in result['reminded']
        assert result.get('already_invited')
        assert result['already_invited'].get('AKBC.ws/2019/Conference/Reviewers/Invited')
        assert 'mbok@mail.com' in result['already_invited'].get('AKBC.ws/2019/Conference/Reviewers/Invited')

        messages = client.get_messages(to = 'mbok@mail.com', subject = 'Reminder: [AKBC 2019]: Invitation to serve as Reviewer')
        text = messages[0]['content']['text']
        assert 'Dear invitee,' in text
        assert 'You have been nominated by the program chair committee of AKBC 2019' in text

        # Test if the mail has "Dear <name>" for unregistered users in case the name is provided to recruit_reviewers
        result = conference.recruit_reviewers(remind = True, invitees = ['mbok2@mail.com'], invitee_names = ['Melisa Bok'])
        assert result
        assert len(result['invited']) == 1
        assert len(result['reminded']) == 3
        assert 'mbok2@mail.com' in result['invited']
        messages = client.get_messages(to = 'mbok2@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        text = messages[0]['content']['text']
        assert 'Dear Melisa Bok,' in text
        assert 'You have been nominated by the program chair committee of AKBC 2019' in text

        # Accept invitation
        messages = client.get_messages(to = 'mbok@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        text = messages[0]['content']['text']
        accept_url = re.search('https://.*response=Yes', text).group(0).replace('https://openreview.net', 'http://localhost:3030')
        request_page(selenium, accept_url, alert=True)

        helpers.await_queue()

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 1
        assert 'mbok@mail.com' in group.members

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        recruit_invitation = re.search(r'https://.*/invitation\?id=(.*)\&user=.*response=Yes', text).group(1)
        recruitment_notes = pc_client.get_notes(invitation = recruit_invitation)
        acceptance_notes = [note for note in recruitment_notes if ('response' in note.content) and (note.content['response'] == 'Yes')]
        assert len(acceptance_notes) == 1

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 1
        assert 'mbok@mail.com' in group.members

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        messages = client.get_messages(to='mbok@mail.com', subject='[AKBC 2019] Reviewer Invitation accepted')
        assert messages
        assert len(messages)
        assert messages[0]['content']['text'] == 'Thank you for accepting the invitation to be a Reviewer for AKBC 2019.\nThe AKBC 2019 program chairs will be contacting you with more information regarding next steps soon. In the meantime, please add noreply@openreview.net to your email contacts to ensure that you receive all communications.\n\nIf you would like to change your decision, please click the Decline link in the previous invitation email.'

        # Reject invitation
        reject_url = re.search('https://.*response=No', text).group(0).replace('https://openreview.net', 'http://localhost:3030')
        request_page(selenium, reject_url, alert=True)

        helpers.await_queue()

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 0

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 1
        assert 'mbok@mail.com' in group.members

        recruitment_notes = pc_client.get_notes(invitation = recruit_invitation)
        acceptance_notes = [note for note in recruitment_notes if 'response' in note.content and note.content['response'] == 'Yes']
        decline_notes = [note for note in recruitment_notes if 'response' in note.content and note.content['response'] == 'No']
        assert len(acceptance_notes) == 1
        assert len(decline_notes) == 1

        messages = client.get_messages(to='mbok@mail.com', subject='[AKBC 2019] Reviewer Invitation declined')
        assert messages
        assert len(messages)
        assert messages[0]['content']['text'] == 'You have declined the invitation to become a Reviewer for AKBC 2019.\n\nIf you would like to change your decision, please click the Accept link in the previous invitation email.\n\n'

        # Accept invitation using encoded user email
        messages = client.get_messages(to = 'mbok@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        text = messages[0]['content']['text']

        accept_url = re.search('https://.*response=Yes', text).group(0).replace('https://openreview.net', 'http://localhost:3030')
        print(accept_url)

        encoded_url = accept_url.split('%40')[0] + '%2540' + accept_url.split('%40')[1]
        request_page(selenium, encoded_url, alert=True)

        helpers.await_queue()

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 1
        assert 'mbok@mail.com' in group.members

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        recruit_invitation = re.search(r'https://.*/invitation\?id=(.*)\&user=.*response=Yes', text).group(1)
        recruitment_notes = pc_client.get_notes(invitation = recruit_invitation)
        acceptance_notes = [note for note in recruitment_notes if ('response' in note.content) and (note.content['response'] == 'Yes')]
        assert len(acceptance_notes) == 2

        messages = client.get_messages(to='mbok@mail.com', subject='[AKBC 2019] Reviewer Invitation accepted')
        assert messages
        assert len(messages) == 2
        assert messages[0]['content']['text'] == 'Thank you for accepting the invitation to be a Reviewer for AKBC 2019.\nThe AKBC 2019 program chairs will be contacting you with more information regarding next steps soon. In the meantime, please add noreply@openreview.net to your email contacts to ensure that you receive all communications.\n\nIf you would like to change your decision, please click the Decline link in the previous invitation email.'

        # Recruit more reviewers
        result = conference.recruit_reviewers(['mbok@mail.com', 'other@mail.com'])
        assert result
        assert len(result['invited']) == 1
        assert 'other@mail.com' in result['invited']

        # Don't send the invitation twice
        messages = client.get_messages(to = 'michael@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        assert messages
        assert len(messages) == 1

        # Remind reviewers
        result = conference.recruit_reviewers(invitees = ['another@mail.com'], invitee_names = ['Mister Another'], remind = True)
        assert result
        assert len(result['invited']) == 1
        assert len(result['reminded']) == 4
        assert 'another@mail.com' in result['invited']
        assert 'other@mail.com' in result['reminded']
        assert 'michael@mail.com' in result['reminded']
        assert 'mohit@mail.com' in result['reminded']
        assert 'mbok2@mail.com' in result['reminded']

        messages = client.get_messages(to = 'another@mail.com', subject = '[AKBC 2019]: Invitation to serve as Reviewer')
        assert messages
        assert len(messages) == 1
        text = messages[0]['content']['text']
        assert 'Dear Mister Another,' in text

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 1

        group = client.get_group('AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        messages = client.get_messages(subject = 'Reminder: [AKBC 2019]: Invitation to serve as Reviewer')
        assert messages
        assert len(messages) == 10
        tos = set([m['content']['to'] for m in messages])
        assert len(tos) == 5
        assert 'michael@mail.com' in tos
        assert 'mohit@mail.com' in tos
        assert 'other@mail.com' in tos
        assert 'mbok@mail.com' in tos
        assert 'mbok2@mail.com' in tos

        # Recruit acs
        result = conference.recruit_reviewers(['mbok@mail.com', 'other@mail.com', 'ac@mail.com'], reviewers_name = 'Area_Chairs')
        assert result
        assert len(result['invited']) == 1
        assert 'ac@mail.com' in result['invited']
        assert result.get('already_invited')
        assert result['already_invited'].get('AKBC.ws/2019/Conference/Reviewers/Invited')
        assert 'mbok@mail.com' in result['already_invited'].get('AKBC.ws/2019/Conference/Reviewers/Invited')
        assert 'other@mail.com' in result['already_invited'].get('AKBC.ws/2019/Conference/Reviewers/Invited')

        group = client.get_group('AKBC.ws/2019/Conference/Area_Chairs')
        assert group
        assert group.id == 'AKBC.ws/2019/Conference/Area_Chairs'
        assert 'AKBC.ws/2019/Conference/Area_Chairs' in group.readers
        assert len(group.members) == 0

        group = client.get_group('AKBC.ws/2019/Conference/Area_Chairs/Invited')
        assert group
        assert len(group.members) == 1

        group = client.get_group('AKBC.ws/2019/Conference/Area_Chairs/Declined')
        assert group
        assert len(group.members) == 0

        messages = client.get_messages(to = 'ac@mail.com', subject = '[AKBC 2019]: Invitation to serve as Area Chair')
        text = messages[0]['content']['text']
        assert 'Dear invitee,' in text
        assert 'You have been nominated by the program chair committee of AKBC 2019' in text

        # accept invitation with invalid user/key keeps group same
        accept_url = re.search('https://.*response=Yes', text).group(0).replace('https://openreview.net', 'http://localhost:3030').replace('ac%40mail.com', 'test%40mail.com')
        request_page(selenium, accept_url, alert=True)

        error_message = selenium.find_element_by_class_name('important_message')
        assert 'Wrong key, please refer back to the recruitment email' == error_message.text

        group = client.get_group('AKBC.ws/2019/Conference/Area_Chairs')
        assert group
        assert len(group.members) == 0

        group = client.get_group('AKBC.ws/2019/Conference/Area_Chairs/Declined')
        assert group
        assert len(group.members) == 0

        notes = client.get_notes(invitation='AKBC.ws/2019/Conference/-/Recruit_Reviewers', content = {'user' : 'test@mail.com'} )
        assert not notes

    def test_set_program_chairs(self, client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        conference = builder.get_result()

        result = conference.set_program_chairs(['pc@mail.com', 'pc2@mail.com'])
        assert result
        assert result.members
        assert ['akbc_pc_1@akbc.ws', 'pc@mail.com', 'pc2@mail.com'] == result.members

        #Sign up as Program Chair
        pc_client = openreview.Client(baseurl = 'http://localhost:3000')
        assert pc_client is not None, "Client is none"
        res = pc_client.register_user(email = 'pc@mail.com', first = 'Pc', last = 'Chair', password = '1234')
        assert res, "Res i none"
        res = pc_client.activate_user('pc@mail.com', {
            'names': [
                    {
                        'first': 'Pc',
                        'last': 'Chair',
                        'username': '~Pc_Chair1'
                    }
                ],
            'emails': ['pc@mail.com'],
            'preferredEmail': 'pc@mail.com'
            })
        assert res, "Res i none"
        group = pc_client.get_group(id = 'pc@mail.com')
        assert group
        assert group.members == ['~Pc_Chair1']

        group = pc_client.get_group(id = 'AKBC.ws/2019/Conference/Reviewers')
        assert group
        assert len(group.members) == 1

        group = pc_client.get_group(id = 'AKBC.ws/2019/Conference/Reviewers/Invited')
        assert group
        assert len(group.members) == 6

        group = pc_client.get_group(id = 'AKBC.ws/2019/Conference/Reviewers/Declined')
        assert group
        assert len(group.members) == 0

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference/Program_Chairs", client.token)
        assert selenium.find_element_by_link_text('Paper Status')
        assert selenium.find_element_by_link_text('Area Chair Status')
        assert selenium.find_element_by_link_text('Reviewer Status')

    def test_close_submission(self, client, test_client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        additional_fields = {
            'archival_status': {
                'description': 'Archival Status.',
                'order': 10,
                'required': False,
                'value-radio': ['Archival', 'Non-Archival'],
            },
            'subject_areas': {
                'description': 'Subject Areas.',
                'order': 12,
                'required': False,
                'values-dropdown': [
                    'Databases',
                    'Information Integration',
                    'Knowledge Representation',
                    'Semantic Web'
                ]
            }
        }
        builder.set_submission_stage(double_blind = True, public = True, additional_fields=additional_fields)
        builder.has_area_chairs(True)
        conference = builder.get_result()

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Submission')
        submission = notes[0]
        submission.content['title'] = 'New paper title'
        test_client.post_note(submission)

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Submission')
        assert 'New paper title' == notes[0].content['title']
        assert '~Test_User1' in notes[0].writers
        assert 'peter@mail.com' in notes[0].writers
        assert 'andrew@mail.com' in notes[0].writers

        request_page(selenium, "http://localhost:3030/forum?id=" + submission.id, test_client.token)

        assert len(selenium.find_elements_by_class_name('edit_button')) == 1
        assert len(selenium.find_elements_by_class_name('trash_button')) == 1

    def test_create_blind_submissions(self, client, test_client):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_conference_name('Automated Knowledge Base Construction')
        builder.set_conference_year(2019)
        additional_fields = {
            'archival_status': {
                'description': 'Archival Status.',
                'order': 10,
                'required': False,
                'value-radio': ['Archival', 'Non-Archival'],
            },
            'subject_areas': {
                'description': 'Subject Areas.',
                'order': 12,
                'required': False,
                'values-dropdown': [
                    'Databases',
                    'Information Integration',
                    'Knowledge Representation',
                    'Semantic Web'
                ]
            }
        }
        builder.set_submission_stage(double_blind = True, public = True, additional_fields=additional_fields)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        conference = builder.get_result()

        conference.setup_post_submission_stage(force=True)

        blind_submissions = conference.get_submissions()
        assert blind_submissions
        assert len(blind_submissions) == 1
        assert blind_submissions[0].content['authors'] == ['Anonymous']
        assert blind_submissions[0].content['authorids'] == ['AKBC.ws/2019/Conference/Paper1/Authors']
        assert blind_submissions[0].content['_bibtex'] == '''@inproceedings{\nanonymous2019new,\ntitle={New paper title},\nauthor={Anonymous},\nbooktitle={Submitted to Automated Knowledge Base Construction},\nyear={2019},\nurl={https://openreview.net/forum?id=''' + blind_submissions[0].id + '''},\nnote={under review}\n}'''

        invitation = client.get_invitation(conference.get_submission_id())
        assert invitation

        note = openreview.Note(invitation = invitation.id,
            readers = [conference.id, '~Test_User1', 'peter@mail.com', 'andrew@mail.com'],
            writers = [conference.id, '~Test_User1', 'peter@mail.com', 'andrew@mail.com'],
            signatures = ['~Test_User1'],
            content = {
                'title': 'Test Paper title',
                'abstract': 'This is a test abstract',
                'authorids': ['test@mail.com', 'peter@mail.com', 'andrew@mail.com'],
                'authors': ['Test User', 'Peter User', 'Andrew Mc'],
                'archival_status': 'Archival',
                'subject_areas': [
                    'Databases',
                    'Information Integration'
                ]
            }
        )
        url = test_client.put_attachment(os.path.join(os.path.dirname(__file__), 'data/paper.pdf'), conference.get_submission_id(), 'pdf')
        note.content['pdf'] = url
        test_client.post_note(note)

        conference.setup_post_submission_stage(force=True)

        blind_submissions_2 = conference.get_submissions()
        assert blind_submissions_2
        assert len(blind_submissions_2) == 2
        assert blind_submissions_2[0].readers == ['everyone']
        assert blind_submissions_2[1].readers == ['everyone']
        assert blind_submissions_2[1].id == blind_submissions[0].id

        note = openreview.Note(invitation = invitation.id,
            readers = [conference.id, '~Test_User1', 'peter@mail.com', 'andrew@mail.com'],
            writers = [conference.id, '~Test_User1', 'peter@mail.com', 'andrew@mail.com'],
            signatures = ['~Test_User1'],
            content = {
                'title': 'Test Paper title 2',
                'abstract': 'This is a test abstract 2',
                'authorids': ['test@mail.com', 'peter@mail.com', 'andrew@mail.com'],
                'authors': ['Test User', 'Peter User', 'Andrew Mc'],
                'archival_status': 'Archival',
                'subject_areas': [
                    'Information Integration'
                ]
            }
        )
        url = test_client.put_attachment(os.path.join(os.path.dirname(__file__), 'data/paper.pdf'), conference.get_submission_id(), 'pdf')
        note.content['pdf'] = url
        test_client.post_note(note)

        conference.setup_post_submission_stage(force=True)

        blind_submissions_3 = conference.get_submissions()
        assert blind_submissions_3
        assert len(blind_submissions_3) == 3
        assert blind_submissions[0].id == blind_submissions_3[2].id
        assert blind_submissions_3[2].readers == ['everyone']

        assert client.get_group('AKBC.ws/2019/Conference/Paper1/Authors')
        assert client.get_group('AKBC.ws/2019/Conference/Paper2/Authors')
        assert client.get_group('AKBC.ws/2019/Conference/Paper3/Authors')

        assert client.get_group('AKBC.ws/2019/Conference/Paper1/Reviewers')
        assert client.get_group('AKBC.ws/2019/Conference/Paper2/Reviewers')
        assert client.get_group('AKBC.ws/2019/Conference/Paper3/Reviewers')

        assert client.get_group('AKBC.ws/2019/Conference/Paper1/Area_Chairs')
        assert client.get_group('AKBC.ws/2019/Conference/Paper2/Area_Chairs')
        assert client.get_group('AKBC.ws/2019/Conference/Paper3/Area_Chairs')

        assert client.get_invitation('AKBC.ws/2019/Conference/Paper1/-/Withdraw')
        assert client.get_invitation('AKBC.ws/2019/Conference/Paper2/-/Withdraw')
        assert client.get_invitation('AKBC.ws/2019/Conference/Paper3/-/Withdraw')

        assert client.get_invitation('AKBC.ws/2019/Conference/Paper1/-/Desk_Reject')
        assert client.get_invitation('AKBC.ws/2019/Conference/Paper2/-/Desk_Reject')
        assert client.get_invitation('AKBC.ws/2019/Conference/Paper3/-/Desk_Reject')

        authors = client.get_group('AKBC.ws/2019/Conference/Authors')
        assert authors
        assert len(authors.members) == 3
        assert 'AKBC.ws/2019/Conference/Paper1/Authors' == authors.members[0]
        assert 'AKBC.ws/2019/Conference/Paper2/Authors' == authors.members[1]
        assert 'AKBC.ws/2019/Conference/Paper3/Authors' == authors.members[2]

    def test_author_groups_inorder(self, client):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        conference = builder.get_result()

        conference_authors_group = client.get_group(id=conference.get_authors_id())
        assert conference_authors_group
        assert len(conference_authors_group.members) == 3
        for num in range(len(conference_authors_group.members)):
            assert conference_authors_group.members[num] == conference.get_authors_id(num+1)

    def test_open_comments(self, client, test_client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        conference = builder.get_result()

        conference.set_comment_stage(openreview.CommentStage(authors=True))

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[0]
        request_page(selenium, "http://localhost:3030/forum?id=" + submission.id, test_client.token)

        reply_row = selenium.find_element_by_class_name('reply_row')
        assert len(reply_row.find_elements_by_class_name('btn')) == 2
        assert 'Official Comment' == reply_row.find_elements_by_class_name('btn')[0].text
        assert 'Withdraw' == reply_row.find_elements_by_class_name('btn')[1].text

    def test_close_comments(self, client, test_client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        conference = builder.get_result()

        conference.close_comments('Official_Comment')

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Submission')
        submission = notes[0]
        request_page(selenium, "http://localhost:3030/forum?id=" + submission.id, test_client.token)

        reply_row = selenium.find_element_by_class_name('reply_row')
        assert len(reply_row.find_elements_by_class_name('btn')) == 1
        assert 'Withdraw' == reply_row.find_elements_by_class_name('btn')[0].text

    def test_open_bids(self, client, test_client, selenium, request_page, helpers):

        reviewer_client = helpers.create_user('reviewer2@mail.com', 'Reviewer', 'DoubleBlind')
        reviewer2_client = helpers.create_user('reviewer@domain.com', 'Reviewer', 'Domain')
        ac_client = helpers.create_user('ac@mail.com', 'AreaChair', 'DoubleBlind')

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        now = datetime.datetime.utcnow()
        builder.set_bid_stage('AKBC.ws/2019/Conference/Reviewers', due_date =  now + datetime.timedelta(minutes = 10), request_count = 50)
        builder.set_bid_stage('AKBC.ws/2019/Conference/Area_Chairs', due_date =  now + datetime.timedelta(minutes = 10), request_count = 50)
        conference = builder.get_result()
        conference.set_area_chairs(emails = ['ac@mail.com'])
        conference.set_reviewers(emails = ['reviewer2@mail.com', 'reviewer@domain.com'])

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Reviewers/-/Bid", reviewer_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 3

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Area_Chairs/-/Bid", ac_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 3

        builder.set_bid_stage('AKBC.ws/2019/Conference/Reviewers', due_date =  now + datetime.timedelta(minutes = 10), request_count = 50, score_ids=['AKBC.ws/2019/Conference/Reviewers/-/Affinity_Score'])
        builder.set_bid_stage('AKBC.ws/2019/Conference/Area_Chairs', due_date =  now + datetime.timedelta(minutes = 10), request_count = 50, score_ids=['AKBC.ws/2019/Conference/Area_Chairs/-/Affinity_Score'])
        conference = builder.get_result()

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Reviewers/-/Bid", reviewer_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 3

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Reviewers/-/Bid", reviewer2_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 3

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Area_Chairs/-/Bid", ac_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 3

        notes = client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[0]

        with open(os.path.join(os.path.dirname(__file__), 'data/reviewer_affinity_scores.csv'), 'w') as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow([submission.id, '~Reviewer_DoubleBlind1', '0.9'])
            writer.writerow([submission.id, '~Reviewer_Domain1', '0.8'])

        conference.setup_matching(affinity_score_file=os.path.join(os.path.dirname(__file__), 'data/reviewer_affinity_scores.csv'), build_conflicts=True)

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Reviewers/-/Bid", reviewer_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert not notes

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Reviewers/-/Bid", reviewer2_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 1

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Area_Chairs/-/Bid", ac_client.token)
        tabs = selenium.find_element_by_class_name('tabs-container')
        assert tabs
        notes = selenium.find_elements_by_class_name('note')
        assert len(notes) == 3

    def test_open_reviews(self, client, test_client, selenium, request_page, helpers):

        now = datetime.datetime.utcnow()
        reviewer_client = openreview.Client(baseurl = 'http://localhost:3000', username='reviewer2@mail.com', password='1234')

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_review_stage(due_date = now + datetime.timedelta(minutes = 10), release_to_authors = True, release_to_reviewers = openreview.ReviewStage.Readers.REVIEWERS_ASSIGNED, email_pcs = True)
        builder.use_legacy_anonids(True)
        conference = builder.get_result()
        conference.set_area_chairs(emails = ['ac@mail.com'])
        conference.set_reviewers(emails = ['reviewer2@mail.com'])

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission', sort='numbers:asc')
        submission = notes[0]

        conference.set_assignment('ac@mail.com', submission.number, is_area_chair = True)
        conference.set_assignment('reviewer2@mail.com', submission.number)

        # Reviewer
        request_page(selenium, "http://localhost:3030/forum?id=" + submission.id, reviewer_client.token)

        reply_row = selenium.find_element_by_class_name('reply_row')
        assert len(reply_row.find_elements_by_class_name('btn')) == 1
        assert 'Official Review' == reply_row.find_elements_by_class_name('btn')[0].text

        # Author
        request_page(selenium, "http://localhost:3030/forum?id=" + submission.id, test_client.token)

        reply_row = selenium.find_element_by_class_name('reply_row')
        assert len(reply_row.find_elements_by_class_name('btn')) == 1
        assert 'Withdraw' == reply_row.find_elements_by_class_name('btn')[0].text

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Official_Review',
            forum = submission.id,
            replyto = submission.id,
            readers = ['AKBC.ws/2019/Conference/Program_Chairs',
            'AKBC.ws/2019/Conference/Paper1/Area_Chairs',
            'AKBC.ws/2019/Conference/Paper1/Reviewers',
            'AKBC.ws/2019/Conference/Paper1/Authors'],
            writers = ['AKBC.ws/2019/Conference/Paper1/AnonReviewer1'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/AnonReviewer1'],
            content = {
                'title': 'Review title',
                'review': 'Paper is very good!',
                'rating': '9: Top 15% of accepted papers, strong accept',
                'confidence': '4: The reviewer is confident but not absolutely certain that the evaluation is correct'
            }
        )
        review_note = reviewer_client.post_note(note)
        assert review_note

        helpers.await_queue()

        process_logs = client.get_process_logs(id = review_note.id)
        assert len(process_logs) == 1
        assert process_logs[0]['status'] == 'ok'

        messages = client.get_messages(subject = '[AKBC 2019] Review posted to your submission - Paper number: 1, Paper title: "New paper title"')
        assert len(messages) == 3
        recipients = [m['content']['to'] for m in messages]
        assert 'test@mail.com' in recipients
        assert 'peter@mail.com' in recipients
        assert 'andrew@mail.com' in recipients

        messages = client.get_messages(subject = '[AKBC 2019] Review posted to your assigned Paper number: 1, Paper title: "New paper title"')
        assert len(messages) == 1
        recipients = [m['content']['to'] for m in messages]
        assert 'ac@mail.com' in recipients

        messages = client.get_messages(subject = '[AKBC 2019] Your review has been received on your assigned Paper number: 1, Paper title: "New paper title"')
        assert len(messages) == 1
        recipients = [m['content']['to'] for m in messages]
        assert 'reviewer2@mail.com' in recipients

        messages = client.get_messages(subject = '[AKBC 2019] A review has been received on Paper number: 1, Paper title: "New paper title"')
        assert len(messages) == 3
        recipients = [m['content']['to'] for m in messages]
        assert 'pc@mail.com' in recipients
        assert 'pc2@mail.com' in recipients
        assert 'akbc_pc_1@akbc.ws' in recipients

        ## Check review visibility
        notes = reviewer_client.get_notes(invitation='AKBC.ws/2019/Conference/Paper1/-/Official_Review')
        assert len(notes) == 1

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/Paper1/-/Official_Review')
        assert len(notes) == 1

    def test_open_revise_reviews(self, client, test_client, selenium, request_page, helpers):

        now = datetime.datetime.utcnow()
        reviewer_client = openreview.Client(baseurl = 'http://localhost:3000', username='reviewer2@mail.com', password='1234')

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        builder.set_conference_short_name('AKBC 2019')
        builder.use_legacy_anonids(True)
        conference = builder.get_result()
        conference.set_area_chairs(emails = ['ac@mail.com'])
        conference.set_reviewers(emails = ['reviewer2@mail.com'])

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[2]

        reviews = test_client.get_notes(invitation='AKBC.ws/2019/Conference/Paper.*/-/Official_Review')
        assert reviews
        review = reviews[0]

        now = datetime.datetime.utcnow()
        conference.open_revise_reviews(due_date = now + datetime.timedelta(minutes = 100))

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/AnonReviewer1/-/Review_Revision',
            forum = submission.id,
            referent = review.id,
            replyto=review.replyto,
            readers = ['AKBC.ws/2019/Conference/Program_Chairs',
            'AKBC.ws/2019/Conference/Paper1/Area_Chairs',
            'AKBC.ws/2019/Conference/Paper1/Reviewers',
            'AKBC.ws/2019/Conference/Paper1/Authors'],
            writers = ['AKBC.ws/2019/Conference', 'AKBC.ws/2019/Conference/Paper1/AnonReviewer1'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/AnonReviewer1'],
            content = {
                'title': 'UPDATED Review title',
                'review': 'Paper is very good!',
                'rating': '9: Top 15% of accepted papers, strong accept',
                'confidence': '4: The reviewer is confident but not absolutely certain that the evaluation is correct'
            }
        )
        review_note = reviewer_client.post_note(note)
        assert review_note

        helpers.await_queue()

        process_logs = client.get_process_logs(id = review_note.id)
        assert len(process_logs) == 1
        assert process_logs[0]['status'] == 'ok'

        messages = client.get_messages(subject = '[AKBC 2019] Revised review posted to your submission: "New paper title"')
        assert len(messages) == 3
        recipients = [m['content']['to'] for m in messages]
        assert 'test@mail.com' in recipients
        assert 'peter@mail.com' in recipients
        assert 'andrew@mail.com' in recipients

        messages = client.get_messages(subject = '[AKBC 2019] Revised review posted to your assigned paper: "New paper title"')
        assert len(messages) == 1
        recipients = [m['content']['to'] for m in messages]
        assert 'ac@mail.com' in recipients

        messages = client.get_messages(subject = '[AKBC 2019] Your revised review has been received on your assigned Paper number: 1, Paper title: "New paper title"')
        assert len(messages) == 1
        recipients = [m['content']['to'] for m in messages]
        assert 'reviewer2@mail.com' in recipients

    def test_open_meta_reviews(self, client, test_client, selenium, request_page, helpers):

        now = datetime.datetime.utcnow()
        ac_client = openreview.Client(baseurl = 'http://localhost:3000', username='ac@mail.com', password='1234')
        assert ac_client is not None, "Client is none"

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_meta_review_stage(due_date = now + datetime.timedelta(minutes = 100))
        builder.use_legacy_anonids(True)
        builder.get_result()

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[2]

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Meta_Review',
            forum = submission.id,
            replyto = submission.id,
            readers = ['AKBC.ws/2019/Conference/Paper1/Area_Chairs', 'AKBC.ws/2019/Conference/Program_Chairs'],
            writers = ['AKBC.ws/2019/Conference/Program_Chairs', 'AKBC.ws/2019/Conference/Paper1/Area_Chairs'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/Area_Chair1'],
            content = {
                'metareview': 'Paper is very good!',
                'recommendation': 'Accept (Oral)',
                'confidence': '4: The area chair is confident but not absolutely certain'
            }
        )
        meta_review_note = ac_client.post_note(note)
        assert meta_review_note

    def test_open_meta_reviews_additional_options(self, client, test_client, selenium, request_page, helpers):

        now = datetime.datetime.utcnow()
        ac_client = helpers.create_user('meta_additional@mail.com', 'TestMetaAdditional', 'User')
        assert ac_client is not None, "Client is none"

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        builder.use_legacy_anonids(True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_meta_review_stage(due_date = now + datetime.timedelta(minutes = 100), additional_fields = {
            'best paper' : {
                'description' : 'Nominate as best paper?',
                'value-radio' : ['Yes', 'No'],
                'required' : True
            }
        })
        conference = builder.get_result()

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[2]

        conference.set_assignment('meta_additional@mail.com', submission.number, is_area_chair = True)

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Meta_Review',
            forum = submission.id,
            replyto = submission.id,
            readers = ['AKBC.ws/2019/Conference/Paper1/Area_Chairs', 'AKBC.ws/2019/Conference/Program_Chairs'],
            writers = ['AKBC.ws/2019/Conference/Program_Chairs', 'AKBC.ws/2019/Conference/Paper1/Area_Chairs'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/Area_Chair2'],
            content = {
                'metareview': 'Excellent Paper!',
                'recommendation': 'Accept (Oral)',
                'confidence': '4: The area chair is confident but not absolutely certain'
            }
        )
        with pytest.raises(openreview.OpenReviewException, match=r'missing'):
            meta_review_note = ac_client.post_note(note)

    def test_open_meta_reviews_remove_fields(self, client, test_client, selenium, request_page, helpers):

        now = datetime.datetime.utcnow()
        ac_client = openreview.Client(baseurl = 'http://localhost:3000', username='meta_additional@mail.com', password='1234')
        assert ac_client is not None, "Client is none"

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.has_area_chairs(True)
        builder.use_legacy_anonids(True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_meta_review_stage(due_date = now + datetime.timedelta(minutes = 100), additional_fields = {
            'best paper' : {
                'description' : 'Nominate as best paper?',
                'value-radio' : ['Yes', 'No'],
                'required' : True
            }
        }, remove_fields = ['confidence'])
        conference = builder.get_result()

        notes = test_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[2]

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Meta_Review',
            forum = submission.id,
            replyto = submission.id,
            readers = ['AKBC.ws/2019/Conference/Paper1/Area_Chairs', 'AKBC.ws/2019/Conference/Program_Chairs'],
            writers = ['AKBC.ws/2019/Conference/Program_Chairs', 'AKBC.ws/2019/Conference/Paper1/Area_Chairs'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/Area_Chair2'],
            content = {
                'metareview': 'Excellent Paper!',
                'recommendation': 'Accept (Oral)',
                'confidence': '4: The area chair is confident but not absolutely certain',
                'best paper': 'Yes'
            }
        )

        with pytest.raises(openreview.OpenReviewException, match=r'Invalid Field'):
            meta_review_note = ac_client.post_note(note)

        note.content = {
            'metareview': 'Excellent Paper!',
            'recommendation': 'Accept (Oral)',
            'best paper': 'Yes'
        }

        meta_review_note = ac_client.post_note(note)
        assert meta_review_note
        assert meta_review_note.content['best paper'] == 'Yes', 'Additional field not initialized'
        assert 'confidence' not in meta_review_note.content, 'Field not removed'

    def test_open_decisions(self, client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_decision_stage()
        builder.set_conference_short_name('AKBC 2019')
        builder.has_area_chairs(True)
        conference = builder.get_result()

        conference.set_program_chairs(emails = ['akbc_pc@mail.com'])

        pc_client = helpers.create_user('akbc_pc@mail.com', 'AKBC', 'Pc')

        accepted_author_group = client.get_group(conference.get_accepted_authors_id())
        assert accepted_author_group
        assert accepted_author_group.members == []

        notes = pc_client.get_notes(invitation='AKBC.ws/2019/Conference/-/Blind_Submission')
        submission = notes[2]

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Decision',
            forum = submission.id,
            replyto = submission.id,
            readers = ['AKBC.ws/2019/Conference/Program_Chairs', 'AKBC.ws/2019/Conference/Paper1/Area_Chairs'],
            nonreaders = ['AKBC.ws/2019/Conference/Paper1/Authors'],
            writers = ['AKBC.ws/2019/Conference/Program_Chairs'],
            signatures = ['AKBC.ws/2019/Conference/Program_Chairs'],
            content = {
                'title': 'Paper Decision',
                'decision': 'Accept (Oral)',
                'comment': 'Great!',
            }
        )

        decision_note = pc_client.post_note(note)
        assert decision_note
        helpers.await_queue()

        accepted_author_group = client.get_group(conference.get_accepted_authors_id())
        assert accepted_author_group
        assert len(accepted_author_group.members) == 1
        assert accepted_author_group.members == [conference.id + '/Paper{}/Authors'.format(submission.number)]

        builder.set_decision_stage(public=True)
        conference = builder.get_result()

        decisions = client.get_notes(invitation = 'AKBC.ws/2019/Conference/Paper.*/-/Decision')
        assert decisions
        assert decisions[0].readers == ['everyone']

        builder.set_decision_stage(release_to_authors=True)
        conference = builder.get_result()

        decisions = client.get_notes(invitation = 'AKBC.ws/2019/Conference/Paper.*/-/Decision')
        assert decisions
        assert decisions[0].readers == ['AKBC.ws/2019/Conference/Program_Chairs', 'AKBC.ws/2019/Conference/Paper1/Area_Chairs', 'AKBC.ws/2019/Conference/Paper1/Authors']

        notes = conference.get_submissions(accepted=True)
        assert notes

    def test_consoles(self, client, test_client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.has_area_chairs(True)
        builder.get_result()

        #Program chair user
        pc_client = openreview.Client(baseurl = 'http://localhost:3000', username='pc@mail.com', password='1234')

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference", pc_client.token)
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('your-consoles')
        assert len(tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')) == 1
        console = tabs.find_element_by_id('your-consoles').find_elements_by_tag_name('ul')[0]
        assert 'Program Chair Console' == console.find_element_by_tag_name('a').text

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference/Program_Chairs#paper-status", pc_client.token)
        assert "AKBC 2019 Conference Program Chairs | OpenReview" in selenium.title
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        assert tabs.find_element_by_id('venue-configuration')
        assert tabs.find_element_by_id('paper-status')
        assert tabs.find_element_by_id('reviewer-status')
        assert tabs.find_element_by_id('areachair-status')

        assert '#' == tabs.find_element_by_id('paper-status').find_element_by_class_name('row-1').text
        assert 'Paper Summary' == tabs.find_element_by_id('paper-status').find_element_by_class_name('row-2').text
        assert 'Review Progress' == tabs.find_element_by_id('paper-status').find_element_by_class_name('row-3').text
        assert 'Status' == tabs.find_element_by_id('paper-status').find_element_by_class_name('row-4').text
        assert 'Decision' == tabs.find_element_by_id('paper-status').find_element_by_class_name('row-5').text

    def test_reassign_reviewers_with_conflict_of_interest(self,client,test_client,selenium,request_page):
        builder=openreview.conference.ConferenceBuilder(client)
        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.has_area_chairs(True)
        builder.use_legacy_anonids(True)
        builder.enable_reviewer_reassignment(True)#enable review reassignment so that the assign_Reviewer_Textbox is rendered on page
        builder.get_result()

        #area chair to reassign reviewer
        ac_client=openreview.Client(baseurl = 'http://localhost:3000', username='ac@mail.com', password='1234')
        request_page(selenium,"http://localhost:3030/group?id=AKBC.ws/2019/Conference/Area_Chairs",ac_client.token)

        show_Reviewers_AnchorTag=selenium.find_element_by_xpath('//*[@id="1-reviewer-progress"]/a')
        selenium.execute_script("arguments[0].click()",show_Reviewers_AnchorTag) #click on "show reviewers anchor tag"
        time.sleep(5) #leave some time for the API and js to complete

        #get the reviewers textbox and click on it to show dropdown
        assign_Reviewer_Textbox_Present=EC.presence_of_element_located((By.XPATH,'//*[@id="1-add-reviewer"]/div/input'))
        WebDriverWait(selenium,5).until(assign_Reviewer_Textbox_Present)
        assign_Reviewer_Textbox=selenium.find_element_by_xpath('//*[@id="1-add-reviewer"]/div/input')
        selenium.execute_script("arguments[0].click()",assign_Reviewer_Textbox)

        #get the dropdown div and check how many dropdown options in it
        dropdown_Options_Present=EC.presence_of_element_located((By.XPATH,'//*[@id="1-add-reviewer"]/div/div'))
        WebDriverWait(selenium,5).until(dropdown_Options_Present)
        dropdown_Options=selenium.find_element_by_xpath('//*[@id="1-add-reviewer"]/div/div')
        assert len(dropdown_Options.find_elements_by_xpath('//*[@id="1-add-reviewer"]/div/div/div'))==1

    def test_open_revise_submissions(self, client, test_client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        additional_fields = {
            'archival_status': {
                'description': 'Archival Status.',
                'order': 10,
                'required': False,
                'value-radio': ['Archival', 'Non-Archival'],
            },
            'subject_areas': {
                'description': 'Subject Areas.',
                'order': 12,
                'required': False,
                'values-dropdown': [
                    'Databases',
                    'Information Integration',
                    'Knowledge Representation',
                    'Semantic Web'
                ]
            }
        }
        builder.set_submission_stage(double_blind = True, public = True, additional_fields=additional_fields)
        builder.set_decision_stage()
        builder.set_conference_short_name('AKBC 2019')
        builder.has_area_chairs(True)
        conference = builder.get_result()

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 3

        assert conference.open_revise_submissions()

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper3/-/Revision',
            forum = notes[0].original,
            referent = notes[0].original,
            readers = ['AKBC.ws/2019/Conference', 'AKBC.ws/2019/Conference/Paper3/Authors'],
            writers = [conference.id, 'AKBC.ws/2019/Conference/Paper3/Authors'],
            signatures = ['AKBC.ws/2019/Conference/Paper3/Authors'],
            content = {
                'title': 'Paper title Revision 2',
                'abstract': 'This is an abstract',
                'authorids': ['test@mail.com', 'peter@mail.com', 'andrew@mail.com'],
                'authors': ['Test User', 'Peter User', 'Andrew Mc'],
                'archival_status': 'Archival',
                'subject_areas': ['Databases'],
                'pdf': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf'
            }
        )

        posted_note = test_client.post_note(note)
        assert posted_note

        assert len(test_client.get_references(referent = notes[0].original)) == 2

    def test_withdraw_submission(self, client, test_client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(
            double_blind=True,
            public=True,
            withdrawn_submission_public=True,
            withdrawn_submission_reveal_authors=True,
            email_pcs_on_withdraw=True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        conference = builder.get_result()
        conference.setup_post_submission_stage(force=True)

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 3

        withdrawal_note = openreview.Note(
            invitation = 'AKBC.ws/2019/Conference/Paper3/-/Withdraw',
            forum = notes[0].forum,
            replyto = notes[0].forum,
            readers = ['everyone'],
            writers = [conference.id + '/Paper{number}/Authors'.format(number = notes[0].number), conference.id],
            signatures = [conference.id + '/Paper{number}/Authors'.format(number = notes[0].number)],
            content = {
                'title': 'Submission Withdrawn by the Authors',
                'withdrawal confirmation': 'I have read and agree with the venue\'s withdrawal policy on behalf of myself and my co-authors.'
            }
        )

        posted_note = test_client.post_note(withdrawal_note)
        assert posted_note

        helpers.await_queue()

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 2

        withdrawn_notes = client.get_notes(invitation=conference.submission_stage.get_withdrawn_submission_id(conference))

        assert len(withdrawn_notes) == 1
        assert withdrawn_notes[0].content.get('_bibtex')
        assert withdrawn_notes[0].content.get('_bibtex') == '@misc{\nuser2019paper,\ntitle={Paper title Revision 2},\nauthor={Test User and Peter User and Andrew Mc},\nyear={2019},\nurl={https://openreview.net/forum?id=' + withdrawn_notes[0].id + '}\n}'

        messages = client.get_messages(subject = '^AKBC 2019: Paper .* withdrawn by paper authors$')
        assert len(messages) == 7
        recipients = [m['content']['to'] for m in messages]
        assert 'test@mail.com' in recipients
        assert 'peter@mail.com' in recipients
        assert 'andrew@mail.com' in recipients
        assert 'pc@mail.com' in recipients
        assert 'akbc_pc_1@akbc.ws' in recipients
        assert 'akbc_pc@mail.com' in recipients
        assert 'pc2@mail.com' in recipients

        author_group = client.get_group('AKBC.ws/2019/Conference/Authors')
        assert author_group
        print(author_group)
        assert len(author_group.members) == 2
        assert 'AKBC.ws/2019/Conference/Paper3/Authors' not in author_group.members

    def test_desk_reject_submission(self, client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(
            double_blind=True,
            public=True,
            desk_rejected_submission_public=True,
            desk_rejected_submission_reveal_authors=True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        conference = builder.get_result()
        conference.setup_post_submission_stage(force=True)

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 2

        desk_reject_note = openreview.Note(
            invitation = 'AKBC.ws/2019/Conference/Paper2/-/Desk_Reject',
            forum = notes[0].forum,
            replyto = notes[0].forum,
            readers = ['everyone'],
            writers = [conference.get_program_chairs_id()],
            signatures = [conference.get_program_chairs_id()],
            content = {
                'desk_reject_comments': 'PC has decided to reject this submission.',
                'title': 'Submission Desk Rejected by Program Chairs'
            }
        )

        pc_client = openreview.Client(baseurl = 'http://localhost:3000', username='pc@mail.com', password='1234')

        posted_note = pc_client.post_note(desk_reject_note)
        assert posted_note

        helpers.await_queue()

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 1

        desk_rejected_notes = client.get_notes(invitation = conference.submission_stage.get_desk_rejected_submission_id(conference))

        assert len(desk_rejected_notes) == 1
        assert desk_rejected_notes[0].content.get('_bibtex')
        assert desk_rejected_notes[0].content.get('_bibtex') == '@misc{\nuser2019test,\ntitle={Test Paper title},\nauthor={Test User and Peter User and Andrew Mc},\nyear={2019},\nurl={https://openreview.net/forum?id=' + desk_rejected_notes[0].id + '}\n}'

        messages = client.get_messages(subject = '^AKBC 2019: Paper .* marked desk rejected by program chairs$')
        assert len(messages) == 7
        recipients = [m['content']['to'] for m in messages]
        assert 'test@mail.com' in recipients
        assert 'peter@mail.com' in recipients
        assert 'andrew@mail.com' in recipients
        assert 'pc@mail.com' in recipients
        assert 'akbc_pc_1@akbc.ws' in recipients
        assert 'akbc_pc@mail.com' in recipients
        assert 'pc2@mail.com' in recipients

        author_group = client.get_group('AKBC.ws/2019/Conference/Authors')
        assert author_group
        print(author_group)
        assert len(author_group.members) == 1
        assert 'AKBC.ws/2019/Conference/Paper2/Authors' not in author_group.members

    def test_paper_ranking(self, client, selenium, request_page):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        conference = builder.get_result()

        now = datetime.datetime.utcnow()
        conference.open_paper_ranking(conference.get_reviewers_id(), due_date = now + datetime.timedelta(minutes = 10))

        reviewer_client = openreview.Client(baseurl = 'http://localhost:3000', username='reviewer2@mail.com', password='1234')

        request_page(selenium, "http://localhost:3030/invitation?id=AKBC.ws/2019/Conference/Reviewer/-/Paper_Ranking", reviewer_client.token)

    def test_edit_revision_as_pc(self, client, test_client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        now = datetime.datetime.utcnow()
        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True, due_date= now - datetime.timedelta(minutes = 60))
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        conference = builder.get_result()

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 1
        note = notes[0]


        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Revision',
            forum = notes[0].original,
            referent = notes[0].original,
            readers = ['AKBC.ws/2019/Conference', 'AKBC.ws/2019/Conference/Paper1/Authors'],
            writers = [conference.id, 'AKBC.ws/2019/Conference/Paper1/Authors'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/Authors'],
            content = {
                'title': 'Paper title REVISED',
                'abstract': 'This is an abstract',
                'authorids': ['test@mail.com', 'peter@mail.com', 'andrew@mail.com'],
                'authors': ['Test User', 'Peter User', 'Andrew Mc'],
                'archival_status': 'Archival',
                'subject_areas': ['Databases'],
                'pdf': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf'
            }
        )

        posted_note = test_client.post_note(note)
        assert posted_note

    def test_release_reviews(self, client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.use_legacy_anonids(True)
        builder.set_conference_year(2019)
        builder.get_result()

        builder.set_review_stage(public=True)
        builder.get_result()

        reviews = client.get_notes(invitation='AKBC.ws/2019/Conference/Paper.*/-/Official_Review')
        assert(reviews)
        assert len(reviews) == 1
        assert reviews[0].readers == ['everyone']

    def test_release_meta_reviews(self, client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.use_legacy_anonids(True)
        builder.set_conference_year(2019)
        builder.set_meta_review_stage(public=True, additional_fields = {
            'best paper' : {
                'description' : 'Nominate as best paper?',
                'value-radio' : ['Yes', 'No'],
                'required' : False
            },
            'confidence': {
                'value-radio': [
                    '5: The area chair is absolutely certain',
                    '4: The area chair is confident but not absolutely certain',
                    '3: The area chair is somewhat confident',
                    '2: The area chair is not sure',
                    '1: The area chair\'s evaluation is an educated guess'
                ],
                'required': False
            }
        })
        builder.get_result()

        reviews = client.get_notes(invitation='AKBC.ws/2019/Conference/Paper.*/-/Meta_Review')
        assert(reviews)
        assert len(reviews) == 2
        assert reviews[0].readers == ['everyone']
        assert reviews[1].readers == ['everyone']

    def test_release_decisions(self, client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        builder.set_decision_stage(public=True)
        builder.get_result()

        decisions = client.get_notes(invitation='AKBC.ws/2019/Conference/Paper.*/-/Decision')
        assert(decisions)
        assert len(decisions) == 1
        assert decisions[0].readers == ['everyone']

    def test_release_accepted_notes(self, client, request_page, selenium):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True)
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_name('Automated Knowledge Base Construction Conference')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        builder.set_decision_stage(public=True)
        conference = builder.get_result()

        conference.post_decision_stage(reveal_authors_accepted=True, decision_heading_map={'Accept (Poster)': 'Accepted poster papers', 'Accept (Oral)': 'Accepted oral papers', 'Reject': 'Reject'})

        request_page(selenium, "http://localhost:3030/group?id=AKBC.ws/2019/Conference")
        assert "AKBC 2019 Conference | OpenReview" in selenium.title
        header = selenium.find_element_by_id('header')
        assert header
        assert "AKBC.ws/2019/Conference" == header.find_element_by_tag_name("h1").text
        invitation_panel = selenium.find_element_by_id('invitation')
        assert invitation_panel
        assert len(invitation_panel.find_elements_by_tag_name('div')) == 0
        notes_panel = selenium.find_element_by_id('notes')
        assert notes_panel
        tabs = notes_panel.find_element_by_class_name('tabs-container')
        assert tabs
        with pytest.raises(NoSuchElementException):
            notes_panel.find_element_by_class_name('spinner-container')
        assert tabs.find_element_by_id('accepted-poster-papers')
        assert tabs.find_element_by_id('accepted-oral-papers')
        assert tabs.find_element_by_id('reject')

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 1
        note = notes[0]

        valid_bibtex = r'''@inproceedings{
user2019paper,
title={Paper title {REVISED}},
author={Test User and Peter User and Andrew Mc},
booktitle={Automated Knowledge Base Construction Conference},
year={2019},
url={'''
        valid_bibtex = valid_bibtex+'https://openreview.net/forum?id='+note.forum+'''}
}'''
        assert note.content['_bibtex'] == valid_bibtex
        assert note.content['venue'] == 'AKBC 2019 Oral'
        assert note.content['venueid'] == 'AKBC.ws/2019/Conference'

        accepted_authors = client.get_group('AKBC.ws/2019/Conference/Authors/Accepted')
        assert accepted_authors
        assert accepted_authors.members == ['AKBC.ws/2019/Conference/Paper1/Authors']

    def test_enable_camera_ready_revisions(self, client, test_client, helpers):

        builder = openreview.conference.ConferenceBuilder(client)
        assert builder, 'builder is None'

        builder.set_conference_id('AKBC.ws/2019/Conference')
        builder.set_submission_stage(double_blind = True, public = True, subject_areas = ['Machine Learning',
            'Natural Language Processing',
            'Information Extraction',
            'Question Answering',
            'Reasoning',
            'Databases',
            'Information Integration',
            'Knowledge Representation',
            'Semantic Web',
            'Search',
            'Applications: Science',
            'Applications: Biomedicine',
            'Applications: Other',
            'Relational AI',
            'Fairness',
            'Human computation',
            'Crowd-sourcing',
            'Other'], additional_fields = {
                'archival_status': {
                    'description': 'Authors can change the archival/non-archival status up until the decision deadline',
                    'value-radio': [
                        'Archival',
                        'Non-Archival'
                    ],
                    'required': True
                }
            })
        builder.set_conference_short_name('AKBC 2019')
        builder.set_conference_name('Automated Knowledge Base Construction Conference')
        builder.set_conference_year(2019)
        builder.has_area_chairs(True)
        builder.set_conference_year(2019)
        builder.set_decision_stage(public=True)
        conference = builder.get_result()

        conference.set_submission_revision_stage(openreview.SubmissionRevisionStage(name='Camera_Ready_Revision', only_accepted=True))

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 1
        note = notes[0]

        note = openreview.Note(invitation = 'AKBC.ws/2019/Conference/Paper1/-/Camera_Ready_Revision',
            forum = notes[0].original,
            referent = notes[0].original,
            readers = ['AKBC.ws/2019/Conference', 'AKBC.ws/2019/Conference/Paper1/Authors'],
            writers = [conference.id, 'AKBC.ws/2019/Conference/Paper1/Authors'],
            signatures = ['AKBC.ws/2019/Conference/Paper1/Authors'],
            content = {
                'title': 'Paper title REVISED AGAIN',
                'abstract': 'This is an abstract',
                'authorids': ['test@mail.com', 'peter@mail.com', 'andrew@mail.com'],
                'authors': ['Test User', 'Peter User', 'Andrew Mc'],
                'archival_status': 'Archival',
                'subject_areas': ['Databases'],
                'pdf': '/pdf/22234qweoiuweroi22234qweoiuweroi12345678.pdf'
            }
        )

        posted_note = test_client.post_note(note)
        assert posted_note

        helpers.await_queue()

        process_logs = client.get_process_logs(id = posted_note.id)
        assert len(process_logs) == 1
        assert process_logs[0]['status'] == 'ok'

        notes = conference.get_submissions()
        assert notes
        assert len(notes) == 1
        note = notes[0]

        assert note.content['title'] == 'Paper title REVISED AGAIN'

        valid_bibtex = r'''@inproceedings{
user2019paper,
title={Paper title {REVISED} {AGAIN}},
author={Test User and Peter User and Andrew Mc},
booktitle={Automated Knowledge Base Construction Conference},
year={2019},
url={'''
        valid_bibtex = valid_bibtex+'https://openreview.net/forum?id='+note.forum+'''}
}'''
        assert note.content['_bibtex'] == valid_bibtex
        assert note.content['venue'] == 'AKBC 2019 Oral'
        assert note.content['venueid'] == 'AKBC.ws/2019/Conference'

        accepted_authors = client.get_group('AKBC.ws/2019/Conference/Authors/Accepted')
        assert accepted_authors
        assert accepted_authors.members == ['AKBC.ws/2019/Conference/Paper1/Authors']
