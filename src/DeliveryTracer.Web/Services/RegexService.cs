using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using DeliveryTracer.Web.Models;

namespace DeliveryTracer.Web.Services
{
    public class RegexService
    {
        private IList<RegexObject> _regexes;
        private readonly AppConfigurations _config;
        
        public RegexService(AppConfigurations config)
        {
            _config = config;

            Init();
        }

        private void Init()
        {
            _regexes = new List<RegexObject>
            {
                new RegexObject
                {
                    Name = "author",
                    Regex = new Regex("(Author).*?(\\n)")
                },
                new RegexObject
                {
                    Name = "commit_id",
                    Regex = new Regex("(commit).*?(\\n)")
                }
            };

        }
        
        public string GetAuthor(string value)
        {
            var regexObj = _regexes.FirstOrDefault(x => x.Name == "author");
            if (regexObj != null)
            {
                if (regexObj.Regex.IsMatch(value))
                    return regexObj.Regex.Match(value).Value.Replace("Author:", "").Replace("\n", "").Trim();
            }

            return value;
        }
        public string GetCommitId(string value)
        {
            var regexObj = _regexes.FirstOrDefault(x => x.Name == "commit_id");
            if (regexObj != null)
            {
                if (regexObj.Regex.IsMatch(value))
                    return regexObj.Regex.Match(value).Value.Replace("commit","").Replace("\n", "").Trim();
            }

            return value;
        }

        public string GetComment(string pattern, string value)
        {
            pattern = pattern + "\n";
            var regex = new Regex(pattern);
            var match = regex.Match(value);

            if (!string.IsNullOrEmpty(match.Value))
                return match.Value.Replace("\n", "");

            return value;
        }
    }
}