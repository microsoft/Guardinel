# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

endpoint_map = {
    'pr_by_id': 'https://dev.azure.com/{}/{}/_apis/git/pullrequests/{}?api-version={}',
    'work_item_by_id': "https://dev.azure.com/{}/_apis/wit/workItems/{}",
    'work_item_by_id_with_relations': "https://dev.azure.com/{}/_apis/wit/workItems/{}?$expand=relations",
    'ado_query_by_id': 'https://dev.azure.com/{}/{}/_apis/wit/queries/{}?api-version={}',
    'ado_query_results_by_id': 'https://dev.azure.com/{}/{}/_apis/wit/wiql/{}',
    'pr_comments': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/pullRequests/{}/threads',
    'pr_commits': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/pullRequests/{}/commits?api-version={}',
    'commit': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/commits/{}?api-version={}',
    'commit_changes': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/commits/{}/changes?api-version={}',
    'get_file_diff': 'https://dev.azure.com/{}/{}/_api/_versioncontrol/fileDiff?__v=5&diffParameters={}'
                     '&repositoryId={}',
    'ado_diff_by_commit': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/diffs/commits',
    'work_item_update_by_id': 'https://dev.azure.com/{}/{}/_apis/wit/workitems/{}',
    'approve_pr_by_id': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/pullrequests/{}/reviewers/{}',
    'repo_branches': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/refs?api-version={}',
    'file_from_commit': 'https://dev.azure.com/{}/{}/_apis/git/repositories/{}/items/{}?versionType=Commit&version={}',
    'create_work_item': 'https://dev.azure.com/{}/{}/_apis/wit/workitems/${}?api-version={}'
}
