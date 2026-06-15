vector_field(x, y, z=0.0) = (-y, x, 0.0)
curl_field(x, y, z=0.0) = (0.0, 0.0, 2.0)
dot_product(a, b) = a[1]*b[1] + a[2]*b[2] + a[3]*b[3]

function boundary_circulation_circle(radius, segments)
    total = 0.0
    for i in 0:(segments-1)
        theta0 = 2*pi*i/segments
        theta1 = 2*pi*(i+1)/segments
        x0, y0 = radius*cos(theta0), radius*sin(theta0)
        x1, y1 = radius*cos(theta1), radius*sin(theta1)
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        total += dot_product(vector_field(xm, ym), (dx, dy, 0.0))
    end
    total
end

function surface_curl_flux_disk(radius, radial_steps)
    total = 0.0
    normal = (0.0, 0.0, 1.0)
    for i in 0:(radial_steps-1)
        r0 = radius*i/radial_steps
        r1 = radius*(i+1)/radial_steps
        ring_area = pi*(r1^2 - r0^2)
        rm = 0.5*(r0+r1)
        total += dot_product(curl_field(rm, 0.0, 0.0), normal)*ring_area
    end
    total
end

function audit_stokes(radius, segments, radial_steps, scenario)
    circulation = boundary_circulation_circle(radius, segments)
    curl_flux = surface_curl_flux_disk(radius, radial_steps)
    warning = (segments < 64 || radial_steps < 16) ? "Coarse boundary or surface sampling; refine before interpreting the theorem comparison." : "Synthetic Stokes theorem audit; document field, surface, boundary, orientation, units, and numerical method."
    return scenario, radius, segments, radial_steps, circulation, curl_flux, abs(circulation-curl_flux), "F=<-y,x,0>; curl F=<0,0,2>", "horizontal disk with upward normal", "counterclockwise boundary orientation viewed from positive z", warning
end

println("scenario,radius,boundary_segments,radial_steps,boundary_circulation,surface_curl_flux,absolute_gap,field_description,surface_description,orientation_note,warning")
for case in [(1.0,32,8,"coarse_audit"),(1.0,128,32,"medium_audit"),(1.0,512,128,"fine_audit")]
    println(join(audit_stokes(case[1], case[2], case[3], case[4]), ","))
end
