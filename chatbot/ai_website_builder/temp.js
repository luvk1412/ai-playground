const openaiApiKey = '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';

async function generateText(prompt) {
    const endpoint = 'https://api.openai.com/v1/completions';
    const data = {
        model: 'gpt-3.5-turbo',
        prompt: prompt,
        max_tokens: 60,
        temperature: 0.5,
    };

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${openaiApiKey}`
        },
        body: JSON.stringify(data)
    };

    try {
        const response = await fetch(endpoint, requestOptions);
        const responseData = await response.json();
        return responseData.choices[0].text;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Example usage:
generateText('Translate the following English text to French: "Hello, how are you?"')
    .then(result => console.log(result));
