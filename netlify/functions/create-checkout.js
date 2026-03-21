exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const secret = process.env.CHARGILY_SECRET_KEY;
  if (!secret) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Clé Chargily manquante' }) };
  }

  try {
    const body = JSON.parse(event.body);

    const res = await fetch('https://pay.chargily.net/api/v2/checkouts', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${secret}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: body.amount * 100,           // 300 DA = 30000 centimes
        currency: 'dzd',
        success_url: body.success_url,
        failure_url: body.failure_url,
        description: body.description || 'Publication annonce PetDZ',
        metadata: body.metadata || {}
      })
    });

    const data = await res.json();

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ checkout_url: data.checkout_url })
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
