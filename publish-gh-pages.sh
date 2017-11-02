#!/usr/bin/env bash

branch=${TRAVIS_BRANCH}
is_pr=${TRAVIS_PULL_REQUEST}
tok="${GITHUB_TOKEN}"
commit="${TRAVIS_COMMIT:0:7}"
DOCS_DIR=$(dirname $0)
trigger_branch="sources"
publish_branch="master"
temp_dir=temp_blog_dir

echo "$branch"
echo "$is_pr"
echo "$commit"
echo "$TRAVIS_JOB_NUMBER"
echo "job no: ${TRAVIS_JOB_NUMBER: -1}"

if [[ "${TRAVIS_JOB_NUMBER: -1}" != "1" ]]; then
    echo "SKIP: Only the first build job publishes the docs."
    exit 0
fi

if [[ "$branch" != "$trigger_branch" || "$is_pr" != "false" ]]; then
    echo "SKIP: Only merges on $trigger_branch branch trigger the publishing to $publish_branch."
    exit 0
fi

git config --global user.email "zoeller.markus@web.de"
git config --global user.name "Markus Zoeller"

cp -R ${DOCS_DIR}/_website $HOME/${temp_dir}

cd $HOME
git clone --branch=${publish_branch} https://${tok}@github.com/markuszoeller/markuszoeller.github.io.git ${publish_branch}

cd ${publish_branch}
rm -rf *  # This is troublesome for custom domain names; add a CNAME file later
cp -Rf ${HOME}/${temp_dir}/* .
echo "https://help.github.com/articles/files-that-start-with-an-underscore-are-missing/" > .nojekyll
echo "www.markusz.io" > CNAME

git add --all -f
git commit -m "Docs build of commit ${commit}"
git log --oneline -5
git push -fq origin ${publish_branch}
