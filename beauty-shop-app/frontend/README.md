
npm install tailwindcss @tailwindcss/vite
npm install react-router-dom
npm install lucide-react


# Beauty Salon & Shop - Frontend Project Structure

```
beauty-salon-shop/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/
│   │   └── images/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Button.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Loader.jsx
│   │   │   └── Alert.jsx
│   │   ├── products/
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductList.jsx
│   │   │   ├── ProductDetail.jsx
│   │   │   └── ProductForm.jsx
│   │   ├── services/
│   │   │   ├── ServiceCard.jsx
│   │   │   ├── ServiceList.jsx
│   │   │   ├── ServiceDetail.jsx
│   │   │   └── BookingForm.jsx
│   │   ├── orders/
│   │   │   ├── Cart.jsx
│   │   │   ├── Checkout.jsx
│   │   │   └── OrderHistory.jsx
│   │   ├── admin/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProductManagement.jsx
│   │   │   ├── ServiceManagement.jsx
│   │   │   ├── OrderManagement.jsx
│   │   │   ├── BookingManagement.jsx
│   │   │   └── Analytics.jsx
│   │   └── auth/
│   │       ├── LoginForm.jsx
│   │       └── RegisterForm.jsx
│   ├── contexts/
│   │   ├── AuthContext.jsx
│   │   └── CartContext.jsx
│   ├── hooks/
│   │   ├── useApi.js
│   │   └── useCart.js
│   ├── layouts/
│   │   ├── MainLayout.jsx
│   │   └── AdminLayout.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── ProductsPage.jsx
│   │   ├── ProductDetailPage.jsx
│   │   ├── ServicesPage.jsx
│   │   ├── BookServicePage.jsx
│   │   ├── CartPage.jsx
│   │   ├── CheckoutPage.jsx
│   │   ├── OrderConfirmationPage.jsx
│   │   ├── OrderHistoryPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── AdminDashboardPage.jsx
│   │   ├── NotFoundPage.jsx
│   │   └── ProfilePage.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── products.js
│   │   ├── services.js
│   │   ├── bookings.js
│   │   └── orders.js
│   ├── utils/
│   │   ├── dateFormatter.js
│   │   ├── priceFormatter.js
│   │   └── validators.js
│   ├── App.jsx
│   ├── main.jsx
│   └── router.jsx
├── .gitignore
├── index.html
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```