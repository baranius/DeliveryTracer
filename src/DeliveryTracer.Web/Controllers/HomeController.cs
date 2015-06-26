using System.Web.Mvc;

namespace DeliveryTracer.Web.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            ViewBag.Host = Request.Url;
            return View();
        }
    }
}
