#!/usr/bin/env node
/* Build S_tpl from a VERIFIED local CSV export of templates.vfs.
 * Do not infer ID semantics from VFS binary layout or a magic filename.
 *
 * CORRECTION R1 (2026-10-11), documented limitations (reproduced synthetically in
 * tests/correction_matrix.test.mjs (case O7); these are HELPER limitations, not defects of the actual
 * Models.bnt archive):
 *  - model archives must be .bnt or .ark; a hypothetical .dat archive is rejected
 *    with an explicit error (this is NOT a claim about any real .dat file);
 *  - only <numeric>.nif entry names contribute to S_model; non-numeric names are
 *    EXCLUDED and now explicitly COUNTED in the output (nonNumericNamesExcluded)
 *    instead of disappearing silently.
 * Historical PCG Models.bnt inventory (earlier measurement, NOT re-opened here):
 * 5596 names <id>.nif, including 218757.nif.
 */
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
function parseCsv(s) { // RFC 4180 quoted CSV, sufficient for exports with embedded commas/CRLF
  let rows=[],cur=[],val='',q=false;
  for(let i=0;i<s.length;i++){let c=s[i];if(q){if(c==='"'&&s[i+1]==='"'){val+='"';i++;}else if(c==='"')q=false;else val+=c;}
  else if(c==='"')q=true;else if(c===','){cur.push(val);val='';}else if(c==='\n'){cur.push(val.replace(/\r$/,''));rows.push(cur);cur=[];val='';}else val+=c;}
  if(q)throw Error('CSV contains unterminated quote');if(val!==''||cur.length){cur.push(val.replace(/\r$/,''));rows.push(cur);}return rows;
}
async function main(argv){
  const o={models:[]};for(let i=0;i<argv.length;i++){let k=argv[i];if(k==='--model-archive'){o.models.push(argv[++i]);continue;}if(['--csv','--id-column','--out','--repo'].includes(k)){o[k.slice(2)]=argv[++i];continue;}throw Error('unknown '+k);}
  if(!o.csv||!o['id-column']||!o.out||!o.repo)throw Error('Usage: node ids_from_export.mjs --csv VERIFIED_TEMPLATES_EXPORT.csv --id-column EXACT_HEADER_NAME --repo EUDORIA_CLEAN_REPO --model-archive Models.bnt [--model-archive Models.ark] --out id_sets.json');
  const csv=parseCsv(fs.readFileSync(o.csv,'utf8'));const hdr=csv.shift(),ix=hdr.indexOf(o['id-column']);if(ix<0)throw Error('Column missing; choose exact export header: '+JSON.stringify(hdr));
  const tpl=[];for(const [j,row] of csv.entries()){const v=row[ix];if(!/^\d+$/.test(v??''))throw Error(`non-decimal template ID row ${j+2}: ${v}`);const n=Number(v);if(!Number.isSafeInteger(n)||n>0xffffffff)throw Error('invalid ID');tpl.push(n);}
  let models=new Set(),modelArchives=[];
  for(const f of o.models){const ext=path.extname(f).toLowerCase();const k=ext==='.bnt'?'Bnt2Archive':ext==='.ark'?'ArkArchive':null;if(!k)throw Error('Model archive must be .bnt or .ark (a .dat archive is not supported by this helper; this is a helper limitation, not a claim about any real archive)');
    const { [k]:Reader }=await import(pathToFileURL(path.join(path.resolve(o.repo),'src/pesource',`${k}.js`)).href);
    const a=new Reader(fs.readFileSync(f));let numeric=0,nonNumeric=0;for(const e of a.entries()){const m=/^(\d+)\.nif$/i.exec(e.name);if(m){models.add(Number(m[1]));numeric++;}else nonNumeric++;}
    modelArchives.push({path:f,nifEntries:numeric,nonNumericNamesExcluded:nonNumeric});}
  const output={S_tpl:[...new Set(tpl)].sort((a,b)=>a-b),S_model:[...models].sort((a,b)=>a-b),S_bvi:[]};
  fs.writeFileSync(o.out,JSON.stringify(output,null,2)+'\n');
  console.log(JSON.stringify({templateRows:tpl.length,uniqueTemplateIds:output.S_tpl.length,modelIds:output.S_model.length,modelArchives,output:o.out,warning:'ID sets are inputs, not proof of any placement relation. Only <numeric>.nif names are counted as model IDs; non-numeric names are excluded and counted in nonNumericNamesExcluded.'},null,2));
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===path.resolve(process.argv[1]))main(process.argv.slice(2)).catch(e=>{console.error(e);process.exitCode=1});