# core/data_exporter.py
"""
Sistema de Exportación de Datos para RAG de Tigo Honduras
Permite exportar resultados RAG a Excel, CSV y otros formatos
"""

import pandas as pd
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import io
import base64


class RAGDataExporter:
    """
    Exportador de datos RAG a múltiples formatos
    """
    
    def __init__(self):
        self.supported_formats = ["excel", "csv", "json", "html"]
    
    def export_rag_response(self, 
                          rag_response: Dict[str, Any], 
                          format_type: str = "excel",
                          include_metadata: bool = True) -> Dict[str, Any]:
        """
        Exporta una respuesta RAG completa a diferentes formatos
        """
        
        if format_type not in self.supported_formats:
            return {"error": f"Formato no soportado. Disponibles: {self.supported_formats}"}
        
        # Extraer datos estructurados de la respuesta
        structured_data = self._extract_structured_data(rag_response)
        
        if format_type == "excel":
            return self._export_to_excel(structured_data, include_metadata)
        elif format_type == "csv":
            return self._export_to_csv(structured_data, include_metadata)
        elif format_type == "json":
            return self._export_to_json(structured_data, include_metadata)
        elif format_type == "html":
            return self._export_to_html(structured_data, include_metadata)
    
    def _extract_structured_data(self, rag_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrae datos estructurados de la respuesta RAG
        """
        answer = rag_response.get("answer", "")
        citations = rag_response.get("citations", [])
        metadata = rag_response.get("metadata", {})
        
        # Extraer datos numéricos del texto de respuesta
        numerical_data = self._extract_numerical_data(answer)
        
        # Crear estructura de datos
        structured_data = {
            "summary": {
                "query_processed": metadata.get("query_intent", "N/A"),
                "total_documents": len(citations),
                "processing_time": metadata.get("processing_time_seconds", 0),
                "confidence": metadata.get("confidence", 0),
                "mode": metadata.get("mode", "unknown"),
                "timestamp": rag_response.get("timestamp", datetime.now().isoformat())
            },
            "documents": self._format_citations_for_export(citations),
            "extracted_data": numerical_data,
            "full_answer": answer,
            "metadata": metadata
        }
        
        return structured_data
    
    def _extract_numerical_data(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrae datos numéricos y porcentajes del texto
        """
        import re
        
        numerical_data = []
        
        # Buscar porcentajes con contexto
        percentage_pattern = r'(\w+[^.]*?)(\d+%)'
        matches = re.findall(percentage_pattern, text)
        
        for i, (context, percentage) in enumerate(matches):
            numerical_data.append({
                "id": f"percentage_{i+1}",
                "type": "percentage",
                "value": percentage,
                "context": context.strip(),
                "category": "demographic" if any(word in context.lower() for word in ["edad", "años", "género", "hombres", "mujeres"]) else "general"
            })
        
        # Buscar datos demográficos específicos
        age_pattern = r'(\d+)\s*a\s*(\d+)\s*años.*?(\d+%)'
        age_matches = re.findall(age_pattern, text)
        
        for i, (age_start, age_end, percentage) in enumerate(age_matches):
            numerical_data.append({
                "id": f"age_group_{i+1}",
                "type": "age_distribution",
                "age_range": f"{age_start}-{age_end} años",
                "percentage": percentage,
                "category": "demographics"
            })
        
        # Buscar ciudades con porcentajes
        city_pattern = r'(Tegucigalpa|San Pedro Sula|Choloma|Comayagua|La Ceiba)[^.]*?(\d+%)'
        city_matches = re.findall(city_pattern, text, re.IGNORECASE)
        
        for i, (city, percentage) in enumerate(city_matches):
            numerical_data.append({
                "id": f"city_{i+1}",
                "type": "geographic_distribution",
                "city": city,
                "percentage": percentage,
                "category": "geography"
            })
        
        return numerical_data
    
    def _format_citations_for_export(self, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formatea las citaciones para exportación
        """
        formatted_citations = []
        
        for i, citation in enumerate(citations):
            formatted_citations.append({
                "id": i + 1,
                "document_name": citation.get("document", "N/A"),
                "study_type": citation.get("study_type", "Unknown"),
                "year": citation.get("year", "N/A"),
                "section": citation.get("section", "N/A"),
                "similarity_score": citation.get("similarity", 0),
                "relevance": "High" if citation.get("similarity", 0) > 0.02 else "Medium" if citation.get("similarity", 0) > 0.01 else "Low"
            })
        
        return formatted_citations
    
    def _export_to_excel(self, data: Dict[str, Any], include_metadata: bool) -> Dict[str, Any]:
        """
        Exporta a Excel con múltiples hojas
        """
        try:
            # Crear buffer en memoria
            output = io.BytesIO()
            
            # Crear writer de Excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                
                # Hoja 1: Resumen
                summary_df = pd.DataFrame([data["summary"]])
                summary_df.to_excel(writer, sheet_name='Resumen', index=False)
                
                # Hoja 2: Documentos fuente
                if data["documents"]:
                    documents_df = pd.DataFrame(data["documents"])
                    documents_df.to_excel(writer, sheet_name='Documentos', index=False)
                
                # Hoja 3: Datos extraídos
                if data["extracted_data"]:
                    extracted_df = pd.DataFrame(data["extracted_data"])
                    extracted_df.to_excel(writer, sheet_name='Datos_Extraidos', index=False)
                
                # Hoja 4: Respuesta completa
                answer_df = pd.DataFrame([{"respuesta_completa": data["full_answer"]}])
                answer_df.to_excel(writer, sheet_name='Respuesta_Completa', index=False)
                
                # Hoja 5: Metadata (si se incluye)
                if include_metadata and data["metadata"]:
                    # Aplanar metadata para DataFrame
                    flattened_metadata = self._flatten_dict(data["metadata"])
                    metadata_df = pd.DataFrame([flattened_metadata])
                    metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            # Obtener datos del buffer
            output.seek(0)
            excel_data = output.getvalue()
            
            # Codificar en base64 para transferencia
            excel_b64 = base64.b64encode(excel_data).decode('utf-8')
            
            return {
                "success": True,
                "format": "excel",
                "filename": f"tigo_rag_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                "data": excel_b64,
                "size_bytes": len(excel_data),
                "sheets": ["Resumen", "Documentos", "Datos_Extraidos", "Respuesta_Completa"] + (["Metadata"] if include_metadata else [])
            }
            
        except Exception as e:
            return {"error": f"Error exportando a Excel: {str(e)}"}
    
    def _export_to_csv(self, data: Dict[str, Any], include_metadata: bool) -> Dict[str, Any]:
        """
        Exporta a CSV (solo datos tabulares principales)
        """
        try:
            # Combinar documentos y datos extraídos en un CSV
            all_data = []
            
            # Agregar documentos
            for doc in data["documents"]:
                all_data.append({
                    "tipo": "documento",
                    "nombre": doc["document_name"],
                    "año": doc["year"],
                    "similaridad": doc["similarity_score"],
                    "relevancia": doc["relevance"],
                    "categoria": "fuente"
                })
            
            # Agregar datos extraídos
            for item in data["extracted_data"]:
                all_data.append({
                    "tipo": "dato_extraido",
                    "nombre": item.get("context", item.get("city", item.get("age_range", "N/A"))),
                    "valor": item.get("value", item.get("percentage", "N/A")),
                    "categoria": item["category"],
                    "tipo_dato": item["type"]
                })
            
            # Crear DataFrame y CSV
            df = pd.DataFrame(all_data)
            csv_data = df.to_csv(index=False)
            
            return {
                "success": True,
                "format": "csv",
                "filename": f"tigo_rag_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "data": csv_data,
                "size_bytes": len(csv_data.encode()),
                "records": len(all_data)
            }
            
        except Exception as e:
            return {"error": f"Error exportando a CSV: {str(e)}"}
    
    def _export_to_json(self, data: Dict[str, Any], include_metadata: bool) -> Dict[str, Any]:
        """
        Exporta a JSON estructurado
        """
        try:
            export_data = {
                "export_info": {
                    "format": "json",
                    "exported_at": datetime.now().isoformat(),
                    "tigo_rag_version": "1.0"
                },
                "summary": data["summary"],
                "documents": data["documents"],
                "extracted_data": data["extracted_data"],
                "full_answer": data["full_answer"]
            }
            
            if include_metadata:
                export_data["metadata"] = data["metadata"]
            
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "format": "json",
                "filename": f"tigo_rag_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                "data": json_data,
                "size_bytes": len(json_data.encode()),
                "structure": list(export_data.keys())
            }
            
        except Exception as e:
            return {"error": f"Error exportando a JSON: {str(e)}"}
    
    def _export_to_html(self, data: Dict[str, Any], include_metadata: bool) -> Dict[str, Any]:
        """
        Exporta a HTML con formato de reporte
        """
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte RAG - Tigo Honduras</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #1E40AF, #3B82F6); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #1E40AF; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #E5E7EB; }}
        th {{ background-color: #F9FAFB; font-weight: 600; color: #374151; }}
        .answer-box {{ background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 20px; border-radius: 5px; }}
        .metric {{ display: inline-block; background: #F0F9FF; padding: 10px 15px; margin: 5px; border-radius: 5px; border: 1px solid #E0F2FE; }}
        .high-relevance {{ color: #059669; font-weight: bold; }}
        .medium-relevance {{ color: #D97706; font-weight: bold; }}
        .low-relevance {{ color: #DC2626; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Reporte de Análisis RAG</h1>
            <p>Tigo Honduras - Inteligencia de Mercado</p>
            <p>Generado: {data['summary']['timestamp']}</p>
        </div>
        
        <div class="section">
            <h2>📋 Resumen Ejecutivo</h2>
            <div class="metric">🎯 Consulta: {data['summary']['query_processed']}</div>
            <div class="metric">📚 Documentos: {data['summary']['total_documents']}</div>
            <div class="metric">⏱️ Tiempo: {data['summary']['processing_time']:.2f}s</div>
            <div class="metric">🎯 Confianza: {data['summary']['confidence']:.0%}</div>
            <div class="metric">🔧 Modo: {data['summary']['mode'].upper()}</div>
        </div>
        
        <div class="section">
            <h2>💡 Respuesta del Sistema</h2>
            <div class="answer-box">
                {data['full_answer'].replace(chr(10), '<br>')}
            </div>
        </div>
        
        <div class="section">
            <h2>📑 Documentos Fuente</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Documento</th>
                        <th>Año</th>
                        <th>Tipo</th>
                        <th>Similaridad</th>
                        <th>Relevancia</th>
                    </tr>
                </thead>
                <tbody>
"""
            
            for doc in data["documents"]:
                relevance_class = f"{doc['relevance'].lower()}-relevance"
                html_content += f"""
                    <tr>
                        <td>{doc['id']}</td>
                        <td>{doc['document_name']}</td>
                        <td>{doc['year']}</td>
                        <td>{doc['study_type']}</td>
                        <td>{doc['similarity_score']:.4f}</td>
                        <td class="{relevance_class}">{doc['relevance']}</td>
                    </tr>
"""
            
            html_content += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📊 Datos Extraídos</h2>
            <table>
                <thead>
                    <tr>
                        <th>Tipo</th>
                        <th>Descripción</th>
                        <th>Valor</th>
                        <th>Categoría</th>
                    </tr>
                </thead>
                <tbody>
"""
            
            for item in data["extracted_data"]:
                description = item.get("context", item.get("city", item.get("age_range", "N/A")))
                value = item.get("value", item.get("percentage", "N/A"))
                html_content += f"""
                    <tr>
                        <td>{item['type'].replace('_', ' ').title()}</td>
                        <td>{description}</td>
                        <td><strong>{value}</strong></td>
                        <td>{item['category'].title()}</td>
                    </tr>
"""
            
            html_content += f"""
                </tbody>
            </table>
        </div>
        
        <div class="section" style="margin-top: 40px; text-align: center; color: #6B7280;">
            <p>📈 Generado por Sistema RAG Tigo Honduras v1.0</p>
            <p>🕐 {datetime.now().strftime('%d/%m/%Y a las %H:%M')}</p>
        </div>
    </div>
</body>
</html>
"""
            
            return {
                "success": True,
                "format": "html",
                "filename": f"tigo_rag_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                "data": html_content,
                "size_bytes": len(html_content.encode()),
                "sections": ["Resumen", "Respuesta", "Documentos", "Datos Extraídos"]
            }
            
        except Exception as e:
            return {"error": f"Error exportando a HTML: {str(e)}"}
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Aplana un diccionario anidado para crear un DataFrame
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        return dict(items)