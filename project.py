from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
app=Flask(__name__)

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
ses=DBsession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = ses.query(Restaurant).filter_by(id=restaurant_id).one()
    items = ses.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

#decorator function
@app.route('/')
@app.route('/restaurants')
def restaurant():
    rests=ses.query(Restaurant).all()
    return render_template('restaurants.html',restaurants=rests)

@app.route('/restaurants/new',methods=['GET','POST'])
def newRestaurant():
    if request.method =='POST':
        newrest=Restaurant(name=request.form['name'])
        ses.add(newrest)
        ses.commmit()
        flash("New Restaurant is added to the database!")
        return redirect(url_for('restaurant'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit',methods=['GET','POST'])
def editrestaurant(restaurant_id):
    rest=ses.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        rest.name=request.form['name']
        ses.add(rest)
        ses.commit()
        flash("Restaurant name is Updated!")
        return redirect(url_for('restaurant'))
    else:
        return render_template('editrestaurant.html',restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete',methods=['GET','POST'])
def deleterestaurant(restaurant_id):
    rest=ses.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method =='POST':
        if rest:
            ses.delete(rest)
            ses.commit()
        return redirect(url_for('restaurant'))
    else:
        return render_template('deleterestaurant.html',restaurant=rest)

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantmenu(restaurant_id):
    menufirst=ses.query(Restaurant).filter_by(id=restaurant_id).one()
    items=ses.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html',restaurant=menufirst,items=items)




# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method =='POST':
        newmenu=MenuItem(name=request.form['name'],description=request.form['description'],price=request.form[price],restaurant_id=restaurant_id)
        ses.add(newmenu)
        ses.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantmenu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)
    #entry=ses.query(MenuItem).filter_by(restaurant_id=restaurant_id)
   
# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    item=ses.query(MenuItem).filter_by(id=menu_id,restaurant_id=restaurant_id).one()
    if request.method == 'POST':        
        if request.form['name']:
            item.name=request.form['name']
        if request.form['description']:
            item.description=request.form['description']
        if request.form['price']:
            item.price=request.form['price']
        if request.form['course']:
            item.price=request.form['course']
        ses.add(item)
        ses.commit()
        flash(" menu item edited!")
        return redirect(url_for('restaurantmenu',restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method=='POST':
        item=ses.query(MenuItem).filter_by(id=menu_id,restaurant_id=restaurant_id).one()
        if item:
            ses.delete(item)
            ses.commit()
            flash("item deleted!")
        return redirect(url_for('restaurantmenu',restaurant_id=restaurant_id))
    else:
        items=ses.query(MenuItem).filter_by(id=menu_id,restaurant_id=restaurant_id).one()
        return render_template('deletemenuitem.html',item=items)

if __name__=='__main__':
    app.secret_key='super-secret-key'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)