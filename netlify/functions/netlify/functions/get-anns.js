exports.handler = async () => {
  try {
    const token = process.env.AIRTABLE_TOKEN;
    const base = process.env.AIRTABLE_BASE_ID;
    const table = process.env.AIRTABLE_TABLE;

    const url = `https://api.airtable.com/v0/\( {base}/ \){table}?sort[0][field]=date&sort[0][direction]=desc`;

    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!response.ok) throw new Error('Airtable fetch failed');

    const data = await response.json();
    const anns = data.records.map(r => ({ id: r.id, ...r.fields }));

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(anns)
    };
  } catch (err) {
    console.error(err);
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
