import { sidebar } from "vuepress-theme-hope";

export default sidebar({
    "/content/": [
        {
            text: "序",
            link: 'Preface',
        },
        'Introduction',
        'Contents',
        {
            text: '第一篇 初级句型--简单句',
            collapsible: false,
            link: 'Part01',
            children: [
                'Chapter01',
                'Chapter02',
                'Chapter03',
                'Chapter04',
                'Chapter05',
                'Chapter06',
                'Chapter07',
                'Chapter08',
                'Chapter09',
                'Chapter10',
                'Chapter11'
            ]
        },
        {
            text: '第二篇 中级句型--复句',
            collapsible: false,
            link: 'Part02',
            children: ['Chapter12', 'Chapter13', 'Chapter14', 'Chapter15']
        },
        {
            text: '第三篇 高级句型--简化从句',
            collapsible: false,
            link: 'Part03',
            children: ['Chapter16', 'Chapter17', 'Chapter18', 'Chapter19', 'Chapter20', 'Chapter21', 'Chapter22']
        },
    ],
});
