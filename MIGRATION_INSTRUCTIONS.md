# Multi-Tenant Migration Instructions

This document provides step-by-step instructions for migrating from the single-tenant restaurant app to the new multi-tenant architecture.

## Steps to Migrate

### 1. First, run the migration script to create the new tables

This will create the Restaurant table and add restaurant_id columns to all related tables:

```
python run_migrations.py
```

### 2. After the tables are created, run the data migration script

This will create the initial restaurant (Shiv Dhaba) and update all existing data to reference this restaurant:

```
python migrate_to_multi_tenant.py
```

### 3. Verify the migration

Check the database to ensure:
- The Restaurant table exists with a "Shiv Dhaba" entry
- All dishes, categories, and orders have been linked to this restaurant
- Try accessing the new URL structure (/{restaurant-slug}/menu)

## New URL Structure

After migration, all URLs will be updated to use the restaurant slug:

### Public URLs
- Restaurant Menu: `/{restaurant-slug}/menu`
- Dish Details: `/{restaurant-slug}/dish/{dish_id}`
- Cart: `/{restaurant-slug}/cart`
- Order Placement: `/{restaurant-slug}/cart/checkout`
- Order Success: `/{restaurant-slug}/order-success/{order_id}`

### Admin URLs
- Admin Dashboard: `/{restaurant-slug}/admin`
- Categories: `/{restaurant-slug}/admin/categories`
- Dishes: `/{restaurant-slug}/admin/dishes`
- Orders: `/{restaurant-slug}/admin/orders`

### Super Admin URLs
- Super Admin Dashboard: `/super-admin`
- Restaurant Management: `/super-admin/restaurants`
- Add Restaurant: `/super-admin/restaurants/add`
- Edit Restaurant: `/super-admin/restaurants/edit/{restaurant_id}`

## Technical Information

The migration implements the following changes:

1. Added a new Restaurant model with fields:
   - name, slug, address, contact_phone, contact_email, description, logo
   
2. Added restaurant_id foreign keys to:
   - Category model
   - Dish model
   - ShivdhabaOrder model
   
3. Updated all routes to be restaurant-scoped with URL patterns

4. Implemented a super admin interface for managing multiple restaurants
