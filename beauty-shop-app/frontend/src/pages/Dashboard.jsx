import { useEffect, useState } from 'react';
import { fetchServices } from '../services/services';

export default function Dashboard() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetchServices().then(setServices);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Services</h1>
      <ul className="space-y-2">
        {services.map(service => (
          <li key={service.id} className="p-4 border rounded shadow">
            {service.name} - ${service.price}
          </li>
        ))}
      </ul>
    </div>
  );
}
