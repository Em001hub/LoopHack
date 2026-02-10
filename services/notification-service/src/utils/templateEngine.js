module.exports = {
    render: (template, data) => template.replace('{{content}}', data.content)
};
