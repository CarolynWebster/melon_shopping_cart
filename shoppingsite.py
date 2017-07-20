"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers


app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)

    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    if 'cart' in session:
        current_cart = session['cart']

        #start with blank total cost and blank order list
        total_cost = 0.0
        all_ordered_melons = []

        #iterate through cart and add total cost and quantity to melon obj
        for item in current_cart:
            #get count from the session cart dictionart
            melon_count = current_cart[item]

            #get melon object using function from melons
            melon_info = melons.get_by_id(item)

            #get price from that melon object
            melon_price = melon_info.price

            #get the total cost of this melon based on count and price
            this_melon_order_total = melon_count * melon_price

            #add quantity attribute to melon object
            melon_info.quantity = melon_count

            #add total cost of this quanitity of this melon to the melon object
            melon_info.indv_total = this_melon_order_total

            #add the total cost of this quantity to the overall total cost
            total_cost += this_melon_order_total

            #add the melon object to the all ordered melons list
            all_ordered_melons.append(melon_info)
    else:
        all_ordered_melons = []
        total_cost = 0
        flash("You haven't selected any melons!")

    return render_template("cart.html",
                            all_melons=all_ordered_melons,
                            order_cost=total_cost)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page

    #get cart from session
    session['cart'] = session.get('cart', {})

    #create var to hold cart dictionary
    current_cart = session['cart']

    #check if melon in the cart, and if not add it
    #if it is increment count
    current_cart[melon_id] = current_cart.get(melon_id, 0) + 1

    #tell user that melon addition is taken care of
    flash("Your melon has successfully added!")

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist
    
    #get inputs of username and password
    username = request.form['email']
    password = request.form['password']

    #check if that email is tied to a customer
    customer = customers.get_by_email(username)

    #get_by_email returns False if customer doesn't exist
    # if customer exists and their password matches
    # log them in and add email to session
    if customer is not False and customer.password == password:
        session['user_email'] = customer.email
        flash("You have successfully logged in!")
        return redirect('/melons')
    else:
        print "elsing!"
        flash("That username or password is incorrect! Try again.")
        return redirect('/login')


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
