Brian Blaylock  
June 8, 2018  
[Homepage](http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html) | 
[Email](mailto:brian.blaylock@utah.edu)

# Python Common Gateway Interface (CGI)

Notes about using Python CGI to dynamically generating webpages and images with Python CGI. This is one way to serve python server-side processing to a webpage.

[CGI Documentation](https://docs.python.org/2/library/cgi.html)

---

## Before you write a script
CGI scripts are configured to only work in a public directory named `cgi-bin/`. For example, your CGI scripts can be in the directory `[your uNID]/public_html/[any path]/cgi-bin/`. The name of your CGI scripts must have the file extension `.cgi`.

## Writing a CGI script
The top line of your `.cgi` file must describe which version of python to use. This is dependent on CHPC's web configuration and version of python. I don't belive you can import just any version of python. The most updated version of Python that allows CGI pages (as far as I know) is `anaconda/4.2.0`. The first line of your script should be:

    #!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

If that doesn't work, try

    #!/usr/local/bin/python

## Using the cgi Python Module
Import the following cgi models

    import sys
    import cgi
    import cgitb
    cgitb.enable()	# Spits out error to browser in coherent format

There are two types of content you will send to the browser. If you are serving a webpage, then you need to set the content type as "HTML". 
    
    print "Content-Type: text/html\n"  
    
If you are serving an image as a PNG, then set the centent type as "PNG".

    print "Content-Type: image/png\n"

> Note: Do not `print` anything when creating an image.

> Debugging Image Scripts: If you are serving and image but get errors, try setting the content type as HTML. This will allow the errors to print in your browser.

If the version of Python does not have a package you need, you can try to import the modules another way. For example, the anaconda distribution does not have `pygrib` installed, but I can import it from another python distribution to it like this:

    sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')

## `matplotlib`
If your script uses `matplotlib` to generate the image, then you must set the backend correctly to essentiall say, "do not open the image in a window."

    import matplotlib as mpl
    mpl.use('Agg')

When you are ready to serve the image to the browser, send it to standard output.

    plt.savefig(sys.stdout)

## Loading data from a form
URLs can carry form data, and you can load form data from a URL into your cgi script. Form data is separated from the main URL a `?`. Individual form items are separated by an `&`. The variable name is given first followed by the value, separated by and `=`. For example:

    http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?model=hrrr&valid=2018-06-08_0000&fxx=0&location=&plotcode=Wind_10-m_Fill&dsize=full&background=arcgis

You load the data like this:
    
    form = cgi.FieldStorage()

    try:
        model = cgi.escape(form['model'].value)
    except:
        model = 'hrrr'

It is a good idea to use the try/except statement, as shown above, in case a form variable did not exist. For example, if the script requires a variable named `model` and the form did not supply a value, then you can set a default value for `model`. 

> Potential Security Vulnerability: The `cgi.escape()` method is very important to prevent a security vulnerability. It convert the characters `&`, `<` and `>` in the input to HTML-safe sequences. Also, be very carful if you execute a `os.system()` command. The input should only be alpha-numeric characters, dashes, numbers, or periods.

## Permissions
In order for the script to be viewable in the browser, you need to set the permissions of the script to be executable by anyone.

    chmod 755 *.cgi

