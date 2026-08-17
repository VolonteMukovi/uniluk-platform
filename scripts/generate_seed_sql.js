/* Génère database/uniluk_seed.sql depuis les données éditoriales du template. */
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const script = html.match(/const PDF_SAMPLE[\s\S]*?\n<\/script>/)[0].replace(/\n<\/script>[\s\S]*/, '');
// Le template est la source des données existantes : l'évaluer évite toute perte lors de l'initialisation SQL.
eval(script);
const data = uniluk();
const esc = v => String(v ?? '').replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\0/g, '');
const val = v => v === null || v === undefined ? 'NULL' : `'${esc(v)}'`;
const json = v => val(JSON.stringify(v || []));
const dateFr = text => {
  const months = {janvier:1,'février':2,mars:3,avril:4,mai:5,juin:6,juillet:7,'août':8,septembre:9,octobre:10,novembre:11,décembre:12};
  const [day, month, year] = text.normalize('NFC').split(' ');
  return `${year}-${String(months[month]).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
};
let sql = `-- Initialisation éditoriale UNILUK\n-- Exécuter après: python manage.py migrate\nSET NAMES utf8mb4;\nSET FOREIGN_KEY_CHECKS=0;\n`;
const insert = (table, cols, rows) => {
  if (!rows.length) return;
  sql += `INSERT IGNORE INTO ${table} (${cols.map(column => `\`${column}\``).join(', ')}) VALUES\n` + rows.map(r => `(${r.map(val).join(', ')})`).join(',\n') + ';\n\n';
};
insert('core_sitesettings', ['id','name','full_name','logo','logo_url','favicon','address','phone','email','maps_url','facebook_url','youtube_url','instagram_url','x_url','footer_text'], [[1,'UNILUK','Université Adventiste de Lukanga','','', '', 'Route de Lukanga, Kamina, RDC','+243 970 000 000','info@uniluk.ac.cd','','','','','','Université Adventiste de Lukanga — ISTA — ISTM. Former des bâtisseurs, corps et esprit, au service du Congo et du monde.']]);
insert('core_heroslide', ['id','image','image_url','tag','title','alt','caption','order','is_published'], data.heroSlides.map((x,i)=>[i+1,'',x.img,x.tag,x.title,x.alt,x.caption,i,1]));
insert('core_statistic', ['id','icon','value','suffix','label','order','is_published'], data.stats.map((x,i)=>[i+1,x.icon,x.value,x.suffix,x.label,i,1]));
insert('core_faculty', ['id','code','name','image','image_url','short_description','description','programs','schedule_file','order','is_published'], data.faculties.map((x,i)=>[x.id,x.code,x.name,'',x.img,x.short,x.full,JSON.stringify(x.options),'',i,1]));
insert('core_article', ['id','category','category_color','title','slug','image','image_url','excerpt','content','published_at','order','is_published'], data.articles.map((x,i)=>[x.id,x.cat,x.catColor,x.title,`article-${x.id}`,'',x.img,x.short,x.full,dateFr(x.date),i,1]));
insert('core_announcement', ['id','tag','color','title','content','published_at','attachment','order','is_published'], data.announcements.map((x,i)=>[x.id,x.tag,x.color,x.title,x.full,dateFr(x.date),'',i,1]));
insert('core_institution', ['id','acronym','color','name','image','image_url','short_description','description','order','is_published'], data.institutions.map((x,i)=>[x.id,x.acronym,x.color,x.name,'',x.img,x.short,x.full,i,1]));
insert('core_studentgroup', ['id','acronym','name','icon','color','image','image_url','description','full_description','achievements','website','contact_email','order','is_published'], data.groups.map((x,i)=>[x.id,x.acronym,x.name,x.icon,x.color,'',x.img,x.desc,x.full,JSON.stringify(x.achievements),x.site,x.contact,i,1]));
insert('core_campusbuilding', ['id','name','description','image','image_url','order','is_published'], data.buildings.map((x,i)=>[x.id,x.name,x.desc,'',x.img,i,1]));
insert('core_service', ['id','section','icon','title','description','order','is_published'], data.clinicServices.map((x,i)=>[i+1,'clinic',x.i,x.t,x.d,i,1]));
insert('core_galleryimage', ['id','title','image','image_url','alt','order','is_published'], data.gallery.map((x,i)=>[i+1,'','',x,'Photo UNILUK',i,1]));
insert('core_testimonial', ['id','quote','name','role','avatar','avatar_url','order','is_published'], data.testimonials.map((x,i)=>[i+1,x.quote,x.name,x.role,'',x.avatar,i,1]));
insert('core_pagecontent', ['id','key','title','subtitle','content','image','image_url','video','video_url'], [
  [1,'campus','Campus & bâtiments','','Découvrez notre campus et ses infrastructures.','','https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=1400&q=80','','https://vjs.zencdn.net/v/oceans.mp4'],
  [2,'eglise','Église Adventiste','','Une vie spirituelle active au cœur du campus.','','https://images.unsplash.com/photo-1438032005730-c779502df39b?w=900&q=80','',''],
  [3,'polyclinique','Polyclinique UNILUK','','Des soins accessibles à la communauté universitaire et environnante.','','https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=900&q=80','',''],
  [4,'admissions','Admissions 2026–2027','Formulaire d’inscription','Merci de compléter soigneusement chaque champ. Notre service des admissions vous contactera sous 72h.','','','',''],
  [5,'about','Une communauté d’apprentissage fondée sur l’excellence et le caractère','À propos de l’UNILUK','Née de la vision de l’Église Adventiste du Septième Jour, l’UNILUK forme des cadres compétents dans les domaines de la théologie, de la gestion, de la santé, de l’éducation et des techniques appliquées. Notre pédagogie associe rigueur scientifique, encadrement personnalisé et développement du caractère.','','https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=900&q=80','','']
]);
sql += 'SET FOREIGN_KEY_CHECKS=1;\n';
fs.mkdirSync('database', {recursive:true});
fs.writeFileSync('database/uniluk_seed.sql', sql, 'utf8');
console.log('database/uniluk_seed.sql généré.');
