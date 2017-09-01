
var list_github_repos_by_user = function(username, success, failure)
{
    var url = 'https://api.github.com/users/' + username + '/repos?sort=updated&direction=desc&type=owner';

    $.get(url,
          function(repos) {
              for (var i = 0; i < repos.length; i++) {
                  if (repos[i].fork) {
                      continue;
                  }
                  var li = '<li><a href="' + repos[i].clone_url + '" target="_blank">' + repos[i].name + '</a></li>';
                    $('ul#repositories').append(li);
              }
          }
    ).fail(function() {
              console.log('error')
          }
    );
}
