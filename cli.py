import click
from fetch_pr import get_pr_data
from summarize import summarize_pr

@click.command()
@click.argument("owner")
@click.argument("repo")
@click.argument("pr_number")
def main(owner, repo, pr_number):
    pr_data = get_pr_data(owner, repo, pr_number)
    summary = summarize_pr(pr_data)
    click.echo(summary)

if __name__ == "__main__":
    main()


#https://github.com/Sachitav03/gh-pr-summarizer/pull/1#issue-3029827410