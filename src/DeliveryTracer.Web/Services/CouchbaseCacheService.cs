using System;
using Couchbase;
using Couchbase.Configuration;
using DeliveryTracer.Web.Models;
using Enyim.Caching.Memcached;
using Newtonsoft.Json;

namespace DeliveryTracer.Web.Services
{
    public interface ICouchbaseCacheService
    {
        void Persist<T>(string key, T value);
        string GetAsString(string key);
        T GetAsObject<T>(string key);
        void Delete(string key);
        bool KeyExists(string key);
    }

    public class CouchbaseCacheService : ICouchbaseCacheService
    {
        private readonly CouchbaseClient _client;

        public CouchbaseCacheService(AppConfigurations config)
        {
            var couchbaseClientConfiguration = new CouchbaseClientConfiguration
            {
                Bucket = config.BucketName
            };

            couchbaseClientConfiguration.Urls.Add(new Uri(config.CouchbaseUrl));

            _client = new CouchbaseClient(couchbaseClientConfiguration);
        }

        public void Persist<T>(string key, T value)
        {
            StoreMode storeMode = GetStoreMode(key);
            string serializeObject = JsonConvert.SerializeObject(value);
            _client.ExecuteStore(storeMode, key, serializeObject);
        }

        private StoreMode GetStoreMode(string key)
        {
            StoreMode storeMode = KeyExists(key) ? StoreMode.Replace : StoreMode.Add;
            return storeMode;
        }

        public string GetAsString(string key)
        {
            if (KeyExists(key))
                return _client.Get<string>(key);

            return "";
        }

        public T GetAsObject<T>(string key)
        {
            if (KeyExists(key))
            {
                string response = _client.Get<string>(key);

                return JsonConvert.DeserializeObject<T>(response);

            }

            return Activator.CreateInstance<T>();
        }

        public void Delete(string key)
        {
            if (KeyExists(key))
                _client.Remove(key);
        }

        public bool KeyExists(string key)
        {
            var obj = _client.Get(key);

            return obj != null;
        }
    }
}