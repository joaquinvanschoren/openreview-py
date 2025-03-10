def process(client, edge, invitation):

    SHORT_PHRASE = ''
    RECRUITMENT_INVITATION_ID = ''
    ASSIGNMENT_INVITATION_ID = ''
    ASSIGNMENT_LABEL = None
    HASH_SEED = ''
    REVIEWERS_INVITED_ID = ''
    PAPER_REVIEWER_INVITED_ID = ''
    INVITED_LABEL = ''
    INVITE_LABEL = ''
    EMAIL_TEMPLATE = ''
    print(edge.id)

    if edge.ddate is None and edge.label == INVITE_LABEL:

        ## Get the submission
        notes=client.get_notes(id=edge.head, details='original')
        if not notes:
            raise OpenReviewException(f'Note not found: {edge.head}')
        submission=notes[0]

        ## - Get profile
        user = edge.tail
        print(f'Get profile for {user}')
        user_profile=openreview.tools.get_profile(client, user)
        inviter_id=openreview.tools.pretty_id(edge.signatures[0])
        inviter_profile=openreview.tools.get_profile(client, edge.tauthor)
        inviter_preferred_name=inviter_profile.get_preferred_name(pretty=True) if inviter_profile else edge.signatures[0]

        if not user_profile:
            user_profile=openreview.Profile(id=user,
                content={
                    'names': [],
                    'emails': [user],
                    'preferredEmail': user
                })

        preferred_name=user_profile.get_preferred_name(pretty=True)

        ## - Build invitation link
        print(f'Send invitation to {user_profile.id}')
        from Crypto.Hash import HMAC, SHA256
        hashkey = HMAC.new(HASH_SEED.encode('utf-8'), msg=user_profile.id.encode('utf-8'), digestmod=SHA256).hexdigest()
        baseurl = 'https://openreview.net' #Always pointing to the live site so we don't send more invitations with localhost

        # build the URL to send in the message
        url = f'{baseurl}/invitation?id={RECRUITMENT_INVITATION_ID}&user={user_profile.id}&key={hashkey}&submission_id={submission.id}&inviter={edge.tauthor}&response='
        accept_url = url + "Yes"
        decline_url = url + "No"

        # format the message defined above
        subject=f'[{SHORT_PHRASE}] Invitation to review paper titled {submission.content["title"]}'
        if EMAIL_TEMPLATE:
            message=EMAIL_TEMPLATE.format(
                title=submission.content['title'],
                abstract=submission.content['abstract'],
                accept_url=accept_url,
                decline_url=decline_url,
                inviter_id=inviter_id,
                inviter_name=inviter_preferred_name,
                inviter_email=edge.tauthor
            )
        else:
            message=f'''Hi {preferred_name},
You were invited to review the paper number: {submission.number}, title: {submission.content['title']}.
Abstract: {submission.content['abstract']}

Please accept the invitation clicking:
{url}Yes

or decline:

{url}No

Thanks,

{inviter_id}
{inviter_preferred_name} ({edge.tauthor})'''

        if PAPER_REVIEWER_INVITED_ID:
            paper_reviewers_invited_id=PAPER_REVIEWER_INVITED_ID.replace('{number}', str(submission.number))
            ## Paper invited group
            client.add_members_to_group(paper_reviewers_invited_id, [user_profile.id])

        if REVIEWERS_INVITED_ID:
            ## General invited group
            client.add_members_to_group(REVIEWERS_INVITED_ID, [user_profile.id])

        ## - Send email
        response = client.post_message(subject, [user_profile.id], message, parentGroup=REVIEWERS_INVITED_ID)

        ## - Update edge to INVITED_LABEL
        edge.label=INVITED_LABEL
        edge.readers=[r if r != edge.tail else user_profile.id for r in edge.readers]
        edge.tail=user_profile.id
        client.post_edge(edge)

